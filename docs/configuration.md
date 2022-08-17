# Configuration

Woke can be configured using optional configuration files. The global configuration file is located in:

- `$HOME/.config/Woke/config.toml` on Linux/MacOS,
- `%USERPROFILE%\Woke\config.toml` on Windows.

Additionally, the configuration file for each project can be located in `{PROJECT_PATH}/woke.toml`.

!!! attention

    Configuration options loaded from TOML files affect only the behavior of the Woke command-line tool.
    LSP configuration options are loaded from LSP clients using the [standard interface](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#workspace_configuration).

## Subconfigs
Any configuration file can include additional configuration files (subconfigs). These subconfigs are loaded after the original configuration file in the specified order. Subconfig configuration values override the values of the parent configuration file.

!!! example "Example woke.toml"
    ```toml
    subconfigs = ["loaded_next.toml", "../relative.toml", "/tmp/absolute.toml", "loaded_last.toml"]
    ```

## Configuration options
The resolution order for each configuration option is:

- default value,
- value in the global configuration file,
- value in the project configuration file.

???+ example "Example woke.toml"
    ```toml
    subconfigs = ["./config1.toml", "config2.toml"]

    [compiler.solc]
    evm_version = "london"
    include_paths = ["node_modules", "lib"]
    remappings = ["@openzeppelin/=node_modules/@openzeppelin/"]
    target_version = "0.8.10"
    via_IR = true

    [compiler.solc.optimizer]
    enabled = true
    runs = 1000
    ```

### `compiler.solc` namespace
`{CWD}` in the following table represents the current working directory (i.e. the directory from which the `woke` command is being executed).

| Option                        | Description                                                                                                                                | Default value                                           |
|:------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------|
| `allow_paths`                 | Allow paths passed to the `solc` executable                                                                                                | `[]`                                                    |
| `evm_version`                 | EVM version as specified by [Solidity docs](https://docs.soliditylang.org/en/latest/using-the-compiler.html#target-options)                | `""` (let the compiler decide)                          |
| `ignore_paths`                | Files in these paths are not compiled unless imported from other non-ignored files                                                         | `[{CWD}/.woke-build, {CWD}/node_modules]`               |
| <nobr>`include_paths`</nobr>  | Paths (along with `{CWD}`) where files from non-relative imports are searched                                                              | `[{CWD}/node_modules]`                                  |
| `remappings`                  | Compiler remappings as specified by [Solidity docs](https://docs.soliditylang.org/en/latest/path-resolution.html#import-remapping)         | `[]`                                                    |
| <nobr>`target_version`</nobr> | Target `solc` version used to compile the project                                                                                          | `""` (use the latest version for each compilation unit) |
| `via_IR`                      | Compile the code via the Yul intermediate language (see [Solidity docs](https://docs.soliditylang.org/en/latest/ir-breaking-changes.html)) | `""` (let the compiler decide)                          |

!!! info
    The `include_paths` option is the preferred way to handle imports of libraries. Remappings should be used only when `include_paths` cannot be used (e.g. when the import path differs from the system path of the imported file).

### `compiler.solc.optimizer` namespace

| Option    | Description                                                                                                                                                                                                                                                        | Default value |
|:----------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------|
| `enabled` | Compile the project with solc optimizations enabled. Leaving this unset disables most of the available optimizations. Setting this to `false` disables all optimizations for Solidity <0.8.6 and has the same behavior as leaving this unset for Solidity >=0.8.6. | `""` (unset)  |
| `runs`    | Configuration of the optimizer specifying how many times the code is intended to be run. Lower values optimize more for initial deployment cost, while higher values optimize more for high-frequency usage.                                                       | `200`         |

### `lsp.find_references` namespace
Configuration options specific to the LSP `Find references` request.

| Option                 | Description                                                     | Default value |
|:-----------------------|:----------------------------------------------------------------|:--------------|
| `include_declarations` | Also include declarations in `Find references` request results. | `false`       |