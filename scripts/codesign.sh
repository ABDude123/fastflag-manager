#!/bin/bash

# Certificate name - replace with your Apple Developer certificate
CERT_NAME="Developer ID Application: Your Name (TEAM_ID)"
APP_PATH="dist/FastFlag Manager.app"
ENTITLEMENTS_PATH="scripts/entitlements.plist"

# Create entitlements file
cat > "$ENTITLEMENTS_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
</dict>
</plist>
EOF

# Sign the app
codesign --force --options runtime --sign "$CERT_NAME" --entitlements "$ENTITLEMENTS_PATH" "$APP_PATH"

# Verify signature
codesign --verify --deep --strict "$APP_PATH" 