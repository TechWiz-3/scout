# Scout

⭐ Find hacktoberfest repos from your CLI by getting repos by the range of stars they have  

Have you noticed that often the best repos to contribute to have somewhere between 5-1000 stars? To find these repos on GitHub however, is quite hard! With scout, this issue ends.  

You can search repos with the exact amount of stars you wish as well as your language and additional optional keywords.

## Install

```
pip install gh-scout
```

Before running `scout`:
1. Create a [GitHub token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), no extra perms are required for the token
2. Create an env variable called `SCOUT_TOKEN`, this will be used to ensure you don't get rate limited by GitHub.
3. Remember to refresh your terminal to load the new env variable
4. Now you're good to go! Run `scout` to start!

![Example](./example.png)
