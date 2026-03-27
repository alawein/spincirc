---
type: canonical
source: none
sync: none
sla: none
---

# Git Repository Shortcuts

## ✅ Installation Complete!

Universal Git workflow shortcuts have been installed and are ready to use.

## 🎯 Available Commands

After opening a new terminal (to load PATH), you can use these commands **in any Git repository**:

```bash
# Before Claude Code session
repo-start        # Pull latest changes and check status

# After Claude Code session  
repo-review       # Review all changes made
repo-stage-all    # Stage all changes for commit
repo-save "msg"   # Stage all + commit + push in one command

# Utilities
repo-help         # Show help and workflow guide
```

## 💡 Typical Workflow

1. **Navigate to your repository:**
   ```bash
   cd /path/to/your/repo
   ```

2. **Before opening Claude Code:**
   ```bash
   repo-start
   ```

3. **Use Claude Code** (make your changes)

4. **After Claude Code session:**
   ```bash
   repo-review                    # See what changed
   repo-save "Add new features"   # Save everything
   ```

## 🔧 Manual Commands (if shortcuts don't work)

If the shortcuts aren't available, use these manual commands:

```bash
# Before Claude
cd /path/to/your/repo
git pull origin main
git status

# After Claude  
git status                           # See changes
git add .                           # Stage all changes
git commit -m "Your message"        # Commit changes
git push origin main                # Push to GitHub
```

## 🌟 Features

- ✅ **Universal**: Works in any Git repository
- ✅ **Automatic**: Handles main/master branch detection
- ✅ **Safe**: Always shows status before major operations
- ✅ **Claude-Clean**: Your Git hook prevents Claude attribution

## 🔄 Loading Scripts

The shortcuts are added to your `~/.bashrc` and will be available in new terminal sessions. If they don't work immediately:

```bash
source ~/.bashrc
```

Or use the direct paths:
```bash
/mnt/c/Users/mesha/Documents/GitHub/SpinCirc/repo-help
```

---

**Ready for Claude Code sessions with clean, organized Git workflows!** 🚀