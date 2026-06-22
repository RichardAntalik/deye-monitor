Never do anything, that is not said to be done.
If you are asked to commit, user must say, that the code works correctly. Never commit otherwise.
When debugging, consider adding debug printfs. It's better to iterate over real data than to endlessly think ooh its' maybe this, but wait, maybe that...

ONLY When user asks you to deploy stuff, Deploy to router.local via scp to path `router.local:/home/me/tools/deye/deye` (path on remote is same as local path)
