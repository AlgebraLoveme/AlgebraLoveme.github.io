<details markdown="1">
<summary>Optional: set or reset the default yourself</summary>

```sh
# Save the economical worker default for a GPT-6.1 Sol main agent.
pira_team config set --main gpt-6.1-sol --model gpt-6-luna --effort max

# Inspect saved defaults.
pira_team config show

# Restore the shipped default for this main model.
pira_team config reset --main gpt-6.1-sol
```

</details>
