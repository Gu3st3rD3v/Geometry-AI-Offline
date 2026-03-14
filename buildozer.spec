name: Geometry-Build
on: [push]

jobs:
  android-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Buildozer-Action
        uses: ArtemSBulgakov/buildozer-action@v1
        with:
          command: buildozer android debug
          buildozer_version: master
        env:
          ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION: true
          FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

      - name: Upload-Artifact
        uses: actions/upload-artifact@v4
        with:
          name: Geometry-AI-APK
          path: bin/*.apk
