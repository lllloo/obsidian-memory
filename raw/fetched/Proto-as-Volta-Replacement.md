---
title: "Setting up Proto as a Volta replacement"
description: 把 moonrepo proto 設定成近似 Volta 行為的六步驟：關 telemetry、auto-install、讀 volta 欄位
created: 2026-09-24
updated: 2026-09-24
source: "https://github.com/TheJaredWilcurt/blog/discussions/41"
published: 2026-01-14
tags:
  - clippings
---

# Setting up Proto as a Volta replacement
2026-01-14T01:16:34Z / 2026-07-30T13:01:13Z
https://github.com/TheJaredWilcurt/blog/discussions/41

This will give you the same functionality Volta offers. Auto-switching/downloading of Node/npm. Ensuring you are never on the wrong version. Letting you pin the Latest or LTS versions of Node/npm. Node/npm versions are set in the repo and get committed. They even have a GitHub Action similar to Volta's.

1. **IMPORTANT! YOU MUST DO THIS FIRST!**
    Create a file in this location: `~/.proto/.prototools` (or `%USERPROFILE%\.proto\.prototools` on Windows) with these contents:
    ```toml
    [settings]
    telemetry = false
    auto-install = true
    ```
1. Install Proto following the instructions on the site:
   * https://moonrepo.dev/docs/proto/install
1. After installed run `proto install node && proto install npm`
   * This step is required to set up the initial shims for Node/npm, without this, auto-install won't work. ([More info](https://github.com/moonrepo/proto/issues/818))
1. From here on out, you should be able to `cd` into any repo and it will check for a Volta object or `devEngines` object in the `package.json`, or `.prototools` file (next to the `package.json`) that looks like this:
   ```toml
   node = "24.1.0"
   npm = "11.7.0"
   ```
1. You can also run any of these commands to update the `.prototools` file.
   * `proto pin node lts --resolve`
   * `proto pin node latest --resolve`
   * `proto pin npm latest --resolve`
1. Or you can skip the need for a `.prototools` file and instead use the official `devEngines` field in the `package.json`:
   * `proto pin node lts --resolve --tool-native`
   * `proto pin node latest --resolve --tool-native`
   * `proto pin npm latest --resolve --tool-native`
1. Go upvote the issue to make telemetry opt-in instead of opt-out:
   * https://github.com/moonrepo/proto/issues/915
1. If you are going to do any global installs (`npm i -g whatever`), you'll need to:
   * Edit `~/.bashrc`
    ```diff
    -export PATH="$PROTO_HOME/shims:$PROTO_HOME/bin:$PATH";
    +export PATH="$PROTO_HOME/shims:$PROTO_HOME/bin:$PROTO_HOME/tools/node/globals/bin:$PATH";
    ```
   * Or add the `~/.proto/tools/node/globals/bin` folder to your PATH manually
