## Configuration



1. Unzip file and place this folder under Package directory (can be found under Sublime-Text -> Preferences -> Browse Packages)


2. One configuration option is available: `indent_size`; which defaults to
`tab_size`, effectively disabling the plugin.

In my case, I have the following in my Syntax Specific settings for C/C++:
Go to Sublime-Text -> Settings -> Settings - Syntax Specific and copy and paste the following lines when you have opened a C/C++ file.
```
{
    "tab_size": 8,
    "indent_size": 3,
    "translate_tabs_to_spaces": false,
    "detect_indentation": false
}
```


3. Open Sublime-Text -> Preferences -> Key Bindings and add these into your setting:
```
[
	{ "keys": ["tab"], "command": "indent_size", "context": [
		{ "key": "auto_complete_visible", "operator": "equal", "operand": false }
	]},
	{ "keys": ["shift+tab"], "command": "insert", "args": {"characters": "\t"} },
	{ "keys": ["backspace"], "command": "backspace_size" },
	{ "keys": ["enter"], "command": "run_macro_file", "args": {"file": "res://Packages/IndentSize/AddLineWithIndentSize.sublime-macro"}, "context":
		[
			{ "key": "setting.auto_indent", "operator": "equal", "operand": true },
			{ "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
			{ "key": "preceding_text", "operator": "regex_contains", "operand": "\\{$", "match_all": true },
			{ "key": "following_text", "operator": "regex_contains", "operand": "^\\}", "match_all": true }
		]
	},
	{ "keys": ["super+]"], "command": "indent_size" },
	{ "keys": ["super+["], "command": "unindent_size" }
	
]
```

Note:

1.tab became reserved for indent only and you need to used shift+tab to insert an actual tab.

2.You should not have indent using space selected in the lower right corner if you have different tab size and indent size.
