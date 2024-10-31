#!/bin/bash

# Required variables
APP_NAME="FastFlag Manager"
DMG_NAME="FastFlagManager-Installer"
APP_PATH="dist/$APP_NAME.app"
DMG_PATH="dist/$DMG_NAME.dmg"
VOLUME_NAME="FastFlag Manager Installer"
BACKGROUND_PATH="resources/dmg/background.png"
ICON_PATH="resources/dmg/volume_icon.icns"

# Create temporary DMG
hdiutil create -srcfolder "$APP_PATH" -volname "$VOLUME_NAME" -fs HFS+ \
        -fsargs "-c c=64,a=16,e=16" -format UDRW -size 200m "dist/temp.dmg"

# Mount the temporary DMG
DEVICE=$(hdiutil attach -readwrite -noverify -noautoopen "dist/temp.dmg" | \
         egrep '^/dev/' | sed 1q | awk '{print $1}')

# Wait for the mount
sleep 2

# Set volume icon
cp "$ICON_PATH" "/Volumes/$VOLUME_NAME/.VolumeIcon.icns"
SetFile -a C "/Volumes/$VOLUME_NAME"

# Set up background
mkdir "/Volumes/$VOLUME_NAME/.background"
cp "$BACKGROUND_PATH" "/Volumes/$VOLUME_NAME/.background/background.png"

# Create Applications symlink
ln -s /Applications "/Volumes/$VOLUME_NAME/Applications"

# Set up custom icons for app and Applications folder
cp "resources/dmg/app_icon.icns" "/Volumes/$VOLUME_NAME/$APP_NAME.app/Contents/Resources/app.icns"
cp "resources/dmg/applications_icon.icns" "/Volumes/$VOLUME_NAME/Applications/.VolumeIcon.icns"

# Set view options with enhanced styling
osascript << EOF
tell application "Finder"
    tell disk "$VOLUME_NAME"
        open
        
        -- Set window properties
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set bounds of container window to {400, 100, 900, 540}
        
        -- Set view options
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 96
        set background picture of theViewOptions to file ".background:background.png"
        set text size of theViewOptions to 12
        set label position of theViewOptions to bottom
        
        -- Position items
        set position of item "$APP_NAME.app" of container window to {150, 220}
        set position of item "Applications" of container window to {450, 220}
        
        -- Custom icon colors and labels
        set label index of item "$APP_NAME.app" of container window to 2 -- Blue
        set label index of item "Applications" of container window to 6 -- Gray
        
        -- Add custom text
        do shell script "echo 'Drag to install' > '/Volumes/$VOLUME_NAME/.install_text'"
        set position of item ".install_text" of container window to {300, 400}
        
        close
        open
        
        -- Wait for background image to load
        delay 2
        
        -- Refresh window
        set position of container window to {400, 100}
        close
        open
        
        update without registering applications
        delay 2
        close
    end tell
end tell
EOF

# Set custom icon permissions
chmod -Rf go-w "/Volumes/$VOLUME_NAME"
sync
sync

# Unmount
hdiutil detach "$DEVICE"

# Convert and compress
hdiutil convert "dist/temp.dmg" -format UDZO -imagekey zlib-level=9 -o "$DMG_PATH"
rm -f "dist/temp.dmg"

# Sign the DMG
codesign --sign "$CERT_NAME" "$DMG_PATH"