🧠 Goal:
When you press Cmd + Space, a Python script will:

📋 Copy selected text

🔁 Switch language layout (ENG ↔ RUS)

📋 Paste the modified text back

 ✅ Step-by-Step Guide
🔧 1. Install Requirements
🟦 Karabiner-Elements
[Install via]  (https://karabiner-elements.pqrs.org)
or
``` brew install Karabiner-Elements ```

🟨 Python + dependencies
Usually preinstalled env on folder
📁 2. Create Python Script
Create file: for example
``` ~/Documents/keyboard-layout-tools/switch_layout_auto.py ```
✅  3. Make it executable:

```chmod +x ~/Documents/keyboard-layout-tools/switch_layout_auto.py```

🧩 4. Add JSON Rule for Karabiner
```~/.config/karabiner/assets/complex_modifications/cmd_space_switch.json```
⚙️ 4. Activate the Rule in Karabiner
**Open Karabiner-Elements**

Go to Complex Modifications

Click "Add rule"

Enable "Cmd+Space switch layout"

🛑 5. Disable macOS default Cmd+Space
Go to:

System Settings → Keyboard → Keyboard Shortcuts

Spotlight / Input Sources

Disable or reassign Cmd+Space

🧪 6. Test It
Select text in any app
Press Cmd+Space

**Have fun!**