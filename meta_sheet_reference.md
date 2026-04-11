# Meta-Sheets and Derived Sheets in VisiData

| Long Name | Keystroke | Scope | Description |
| :---- | :---- | :---- | :---- |
| **CommandLog** |  |  |  |
| `cmdlog-sheet` | `Shift+D` | Sheet | Open current sheet's CommandLog (includes parent sheets) |
| `cmdlog-sheet-only` | `zShift+D` | Sheet | Open CommandLog for current sheet (parent sheets removed) |
| `cmdlog-all` | `gShift+D` | Session | Open global CommandLog for all commands in session |
| **Columns** |  |  |  |
| `columns-sheet` | `Shift+C` | Sheet | Edit column properties for current sheet |
| `columns-all` | `gShift+C` | Session | Edit column properties for all visible columns from all sheets |
| `columns-selected` | `gShift+C` *(IndexSheet only)* | Session | Open Columns Sheet with all visible columns from selected sheets |
| **Data Cleaning** |  |  |  |
| `dedupe-rows` | *(none)* | Sheet | Open new sheet with only non-duplicate rows |
| `freeze-sheet` | `g'` | Sheet | Open frozen copy with all visible columns evaluated |
| `random-rows` | *(none)* | Sheet | Open duplicate sheet with a random subset of N rows |
| **Describe** |  |  |  |
| `describe-sheet` | `Shift+I` | Sheet | View summary statistics for all visible columns |
| `describe-all` | `gShift+I` | Session | View statistics for all visible columns from all sheets |
| `describe-selected` | `gShift+I` *(IndexSheet only)* | Session | View statistics for all visible columns from selected sheets |
| **Duplicate** |  |  |  |
| `dup-selected` | `"` | Sheet | Open duplicate sheet with only selected rows |
| `dup-rows` | `g"` | Sheet | Open duplicate sheet with all rows |
| `dup-selected-deep` | `z"` | Sheet | Open duplicate with deepcopy of selected rows |
| `dup-rows-deep` | `gz"` | Sheet | Open duplicate with deepcopy of all rows |
| **Errors** |  |  |  |
| `error-recent` | `Ctrl+E` | Session | View traceback for most recent error |
| `errors-all` | `gCtrl+E` | Session | View traceback for all recent errors |
| `error-cell` | `zCtrl+E` | Sheet | View traceback for error in current cell |
| **Frequency** |  |  |  |
| `freq-col` | `Shift+F` | Sheet | Open Frequency Table grouped on current column |
| `freq-keys` | `gShift+F` | Sheet | Open Frequency Table grouped by all key columns |
| `freq-summary` | `zF` | Sheet | Open one-line summary for all rows and selected rows |
| **Help** |  |  |  |
| `help-commands` | `zCtrl+H` | Sheet | List commands and keybindings for current sheet |
| `help-commands-all` | `gzCtrl+H` | Session | List commands and keybindings for all sheet types |
| `sysopen-help` | `gCtrl+H` | General | Show UNIX man page for VisiData |
| `open-guide-index` | *(none)* | General | Open VisiData guides table of contents |
| **Macros** |  |  |  |
| `macro-sheet` | `gm` | Session | Open index of existing macros |
| **Melt** |  |  |  |
| `melt` | `Shift+M` | Sheet | Open Melted Sheet (unpivot), key columns retained |
| `melt-regex` | `gShift+M` | Sheet | Open Melted Sheet with regex capture groups for column names |
| **Navigation** |  |  |  |
| `open-row` | `Enter` | Sheet | Open current row with sheet-specific dive |
| `open-row-basic` | *(none)* | Sheet | Dive into current row as basic table (ignoring custom dive) |
| `open-cell` | `zEnter` | Sheet | Open sheet with copies of rows referenced in current cell |
| `open-source` | `` ` `` | Sheet | Open source sheet |
| `open-source-next` | `g>` | Session | Open next sheet on parent index sheet |
| `open-source-prev` | `g<` | Session | Open prev sheet on parent index sheet |
| `undo-last-quit` | `gShift+U` | Session | Reopen most recently closed sheet |
| **Options** |  |  |  |
| `options-global` | `Shift+O` | Configuration | Edit global options (apply to all sheets) |
| `options-sheet` | `zShift+O` | Sheet | Edit sheet options (apply to current sheet only) |
| `open-config` | `gShift+O` | Configuration | Open options.config as text sheet |
| **Pivot** |  |  |  |
| `pivot` | `Shift+W` | Sheet | Open Pivot Table: group rows by key column and summarize current column |
| **Python/Introspection** |  |  |  |
| `pyobj-sheet` | `gCtrl+Y` | Sheet | Open current sheet as Python object |
| `open-sidebar` | `gb` | Sheet | Open sidebar content in new sheet |
| **Scrape** |  |  |  |
| `scrape-cells` | `gzo` | Sheet | Open HTML Documents sheet from selected URLs |
| **Sheets** |  |  |  |
| `sheets-stack` | `Shift+S` | Session | Open Sheets Stack: jump between active sheets |
| `sheets-all` | `gShift+S` | Session | Open Sheets Sheet: all sheets from current session |
| `open-new` | `Shift+A` | General | Open new empty sheet |
| **Status/Threads** |  |  |  |
| `open-statuses` | `Ctrl+P` | Session | Open Status History |
| `threads-all` | `Ctrl+T` | Session | Open Threads for all sheets |
| `threads-sheet` | `zCtrl+T` | Sheet | Open Threads for this sheet |
| **Transform** |  |  |  |
| `transpose` | `Shift+T` | Sheet | Open new sheet with rows and columns transposed |
| **Utilities** |  |  |  |
| `open-colors` | *(none)* | Configuration | Open Color Sheet with available terminal colors |
| `open-palettes` | *(none)* | Configuration | Open color palettes sheet for graphs |
| `open-dir-current` | *(none)* | General | Open Directory Sheet: browse files in current directory |
| `open-input-history` | `open-inputs` | Session | Open sheet with previous inputs |
| `open-memos` | `Alt+Shift+M` | General | Open the Memory Sheet |
| `open-ping` | *(none)* | General | Open sheet to ping an IP address |
| `open-plugins` | *(none)* | Configuration | Open Plugins Sheet to manage supported plugins |
| `open-python-packages` | *(none)* | Configuration | Open Python Packages Sheet listing installed packages |

## Notes

- **Sheet scope**: Sheets that operate on or derive from the current sheet  
- **Session scope**: Sheets that provide information about the current VisiData session  
- **Configuration scope**: Sheets for managing user configuration, colors, and themes  
- **General scope**: Sheets that provide general utility functions

Derived sheets are created from existing sheets and provide different views or aggregations of the data. The "dive into" commands allow you to explore subsets of your data by opening new sheets containing specific rows or groups.
