# Meta-Sheets and Derived Sheets in VisiData

| Meta-Sheet Name | Keystroke Command(s) | Long Name Command(s) | Scope | Description |
| :---- | :---- | :---- | :---- | :---- |
| **Meta-Sheets** |  |  |  |  |
| Columns Sheet | `Shift+C` | `columns-sheet` | Sheet | Edit column properties of current sheet |
|  | `gC` | `columns-all` | Session | Edit columns from all visible sheets |
| Sheets Sheet | `Shift+S` | `sheets-stack` | Session | Jump between active sheets on current stack |
|  | `gS` | `sheets-all` | Session | All sheets from current session (active and inactive) |
| Options Sheet | `Shift+O` | `options-global` | Configuration | Edit global options (apply to all sheets) |
|  | `zO` | `options-sheet` | Sheet | Edit sheet options (apply to current sheet only) |
|  | `gO` | `options-config` | Configuration | Open options.config as TextSheet |
| CommandLog | `Shift+D` | `cmdlog-sheet` | Sheet | Current sheet's CommandLog (includes parent sheets) |
|  | `gD` | `cmdlog-all` | Session | Global CommandLog for all commands in session |
|  | `zD` | `cmdlog-sheet-only` | Sheet | Current sheet's CommandLog (parent sheets removed) |
| Error Sheet | `Ctrl+E` | `error-sheet` | Session | View last error |
|  | `z^E` | `error-cell` | Sheet | View traceback for error in current cell |
| Status History | `Ctrl+P` | `status-history` | Session | View history of status messages |
| Threads Sheet | `Ctrl+T` | `threads-all` | Session | View all asynchronous threads running |
|  | `z^T` | `threads-sheet` | Sheet | View current sheet's threads |
| Directory Sheet | `Space` | `open-dir-current` | General | Browse files in current directory |
| Guide Index | `Space` | `open-guide-index` | General | Read documentation within VisiData |
| Memory Sheet | `Alt+Shift+M` | `memory-sheet` | General | Browse saved values, including clipboard |
| Colors Sheet | (none) | `open-colors` | Configuration | View all 256 available colors and current color settings |
| Help Sheet | `z^H` | `help-commands` | Sheet | List commands and keybindings for current sheet |
|  | `gz^H` | `help-commands-all` | Session | List commands and keybindings for all sheet types |
|  | `g^H` | `sysopen-help` | General | Show UNIX man page for VisiData |
| Macro Sheet | `gm` | `macros-sheet` | Session | Open index of all user-defined macros |
| Types Sheet | (none) | `types-sheet` | Configuration | View and manage column types |
| Themes Sheet | (none) | `themes-sheet` | Configuration | Change interface theme |
| **Derived Sheets** |  |  |  |  |
| Frequency Table | `Shift+F` | `freq-col` | Sheet | Group rows by current column with aggregations |
|  | `gF` | `freq-keys` | Sheet | Group rows by all key columns |
|  | `zF` | `freq-summary` | Sheet | One-line summary for all rows and selected rows |
| Describe Sheet | `Shift+I` | `describe-sheet` | Sheet | View summary statistics for current sheet's columns |
|  | `gI` | `describe-all` | Session | View statistics for all visible columns from all sheets |
| Pivot Table | `Shift+W` | `pivot-col` | Sheet | Group rows by key and summarize current column |
| Melted Sheet | `Shift+M` | `melt-sheet` | Sheet | Unpivot non-key columns into variable/value columns |
|  | `gM` | `melt-sheet-regex` | Sheet | Melt with regex pattern for column names |
| Transposed Sheet | `Shift+T` | `transpose-sheet` | Sheet | Open new sheet with rows and columns transposed |
| **Dive Into/Subset Sheets** |  |  |  |  |
| Dive into Row | `Enter` | `open-row` | Sheet | Open sheet with rows grouped in current row (frequency/pivot) |
| Dive into Cell | `zEnter` | `open-cell` | Sheet | Open sheet with rows for current cell value |
| Dive into Selected | `gEnter` | `open-selected` | Sheet | Open sheet with rows from selected rows |
| Duplicate Selected | `"` | `dup-selected` | Sheet | Open duplicate sheet with only selected rows |
| Duplicate All | `g"` | `dup-rows` | Sheet | Open duplicate sheet with all rows |
| Duplicate Selected Deep | `z"` | `dup-selected-deep` | Sheet | Open duplicate with deepcopy of selected rows |
| Duplicate All Deep | `gz"` | `dup-rows-deep` | Sheet | Open duplicate with deepcopy of all rows |

## Notes

- **Sheet scope**: Sheets that operate on or derive from the current sheet  
- **Session scope**: Sheets that provide information about the current VisiData session  
- **Configuration scope**: Sheets for managing user configuration, colors, and themes  
- **General scope**: Sheets that provide general utility functions

Derived sheets are created from existing sheets and provide different views or aggregations of the data. The "dive into" commands allow you to explore subsets of your data by opening new sheets containing specific rows or groups.
