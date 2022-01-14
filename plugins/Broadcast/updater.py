import os 
from asyncio import sleep as rest 
import asyncio
from git import Repo
from git.exc import GitCommandError
from pyrogram import Client, filters 
UPSTREAM_REPO =https://github.com/M-DEVAMARIA/venom.git
UPSTREAM_REMOTE = "Version_2.0"

@Client.on_message(filters.command(['update', 'update']))
async def check_update(bot, message):
    """ check or do updates """
    await message.edit("`Checking for updates, please wait....`")
    flags = list(message.flags)
    pull_from_repo = False
    branch = "master"
    if "pull" in flags:
        pull_from_repo = True
        flags.remove("pull")
    if len(flags) == 1:
        branch = flags[0]
        dev_branch = "alpha"
        if branch == dev_branch:
            await message.err('Can\'t update to unstable [alpha] branch. '
                              'Please use other branches instead !')
            return
    repo = Repo()
    if branch not in repo.branches:
        await message.err(f'invalid branch name : {branch}')
        return
    try:
        out = _get_updates(repo, branch)
    except GitCommandError as g_e:
        await message.err(g_e, del_in=5)
        return
    if pull_from_repo:
        if out:
            await message.edit(f'`New update found for [{branch}], Now pulling...`')
            await _pull_from_repo(repo, branch)
            await CHANNEL.log(f"**PULLED update from [{branch}]:\n\n📄 CHANGELOG 📄**\n\n{out}")
            await message.edit('**Userge Successfully Updated!**\n'
                               '`Now restarting... Wait for a while!`', del_in=3)
            asyncio.get_event_loop().create_task(userge.restart(True))
        else:
            active = repo.active_branch.name
            if active == branch:
                await message.err(f"already in [{branch}]!")
                return
            await message.edit(
                f'`Moving HEAD from [{active}] >>> [{branch}] ...`', parse_mode='md')
            await _pull_from_repo(repo, branch)
            await CHANNEL.log(f"`Moved HEAD from [{active}] >>> [{branch}] !`")
            await message.edit('`Now restarting... Wait for a while!`', del_in=3)
            asyncio.get_event_loop().create_task(userge.restart())
    elif out:
        change_log = f'**New UPDATE available for [{branch}]:\n\n📄 CHANGELOG 📄**\n\n'
        await message.edit_or_send_as_file(change_log + out, disable_web_page_preview=True)
    else:
        await message.edit(f'**Userge is up-to-date with [{branch}]**', del_in=5)


def _get_updates(repo: Repo, branch: str) -> str:
    repo.remote(UPSTREAM_REMOTE).fetch(branch)
    upst = UPSTREAM_REPO.rstrip('/')
    return ''.join(
        f"🔨 **#{i.count()}** : [{i.summary}]({upst}/commit/{i}) 👷 __{i.author}__\n\n"
        for i in repo.iter_commits(f'HEAD..{UPSTREAM_REMOTE}/{branch}')
    )


async def _pull_from_repo(repo: Repo, branch: str) -> None:
    repo.git.checkout(branch, force=True)
    repo.git.reset('--hard', branch)
    repo.remote(UPSTREAM_REMOTE).pull(branch, force=True)
    await asyncio.sleep(1)
