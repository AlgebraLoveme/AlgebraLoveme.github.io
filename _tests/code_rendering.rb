# frozen_string_literal: true

require "jekyll"
require "rexml/document"

ROOT = File.expand_path("..", __dir__)
config = Jekyll.configuration("source" => ROOT, "quiet" => true)
converter = Jekyll::Converters::Markdown.new(config)

def assert(condition, message)
  abort "FAIL: #{message}" unless condition
end

def body(path)
  File.read(path).sub(/\A---\s*\n.*?^---\s*\n/m, "")
end

def text_of(element)
  element.children.map { |child| child.is_a?(REXML::Element) ? text_of(child) : child.value }.join
end

fixture = body(File.join(ROOT, "_tests/fixtures/code-blocks.md"))
html = converter.convert(fixture)
document = REXML::Document.new("<root>#{html}</root>")
blocks = REXML::XPath.match(document, "//pre/code")
expected = fixture.scan(/^```[^\n]*\n(.*?)^```/m).flatten
assert(blocks.map { |block| text_of(block) } == expected, "fenced code preserves literal text, indentation, tabs and long lines")
assert(REXML::XPath.match(document, "//script").empty?, "code never creates script elements")
assert(html.include?("&lt;script&gt;") && html.include?("&amp;"), "HTML characters are escaped")
%w[sh python].each do |language|
  wrappers = REXML::XPath.match(document, "//div[@class='language-#{language} highlighter-rouge']")
  assert(!wrappers.empty?, "#{language} uses the Rouge wrapper")
  assert(wrappers.all? { |wrapper| !REXML::XPath.match(wrapper, ".//span").empty? }, "#{language} has syntax tokens")
end
assert(blocks[2..3].all? { |block| REXML::XPath.match(block, ".//span").empty? }, "text and unlabelled fences remain unhighlighted")
assert(REXML::XPath.match(document, "//p/code").size == 1, "inline code remains outside pre")
details = REXML::XPath.match(document, "//details")
assert(details.size == 1, "code cannot close the disclosure early")
assert(REXML::XPath.match(details.first, ".//pre/code").size == 1, "disclosure contains its highlighted fence")
assert(REXML::XPath.first(details.first, "summary").text == "Optional commands", "summary remains HTML")
assert(REXML::XPath.first(details.first, "p/strong").text == "the disclosure", "selected container parses Markdown")
assert(REXML::XPath.match(details.first, ".//h2").empty? && REXML::XPath.first(document, "/root/h2").text == "After the disclosure", "following content stays outside disclosure")
assert(html.include?("**Unparsed HTML stays literal.**"), "HTML parsing is not enabled globally")

post = body(File.join(ROOT, "_posts/2026-10-10-working-with-pira-team.md"))
disclosure = post[/<details[^>]*>.*?<\/details>/m]
assert(disclosure, "Team disclosure exists")
rendered = REXML::Document.new("<root>#{converter.convert(disclosure)}</root>")
code = REXML::XPath.first(rendered, "//details//pre/code")
assert(code && !REXML::XPath.match(code, ".//span").empty?, "actual Team disclosure is highlighted")
assert(text_of(code) == <<~SHELL, "Team commands and comments remain unchanged")
  # Save the economical worker default for a GPT-6.1 Sol main agent.
  pira_team config set --main gpt-6.1-sol --model gpt-6-luna --effort max

  # Inspect saved defaults.
  pira_team config show

  # Restore the shipped default for this main model.
  pira_team config reset --main gpt-6.1-sol
SHELL
puts "PASS: Kramdown/GFM + Rouge fences, escaping, whitespace, inline code, disclosure boundaries and unchanged Team commands"
