; installer.nsi
; This script creates an NSIS installer for the Lite Agent CLI.

; General Installer Settings
Name "Lite Agent CLI"
; Use the ARCH define from makensis command line for dynamic OutFile name
OutFile "LiteAgentCLI_Installer_${ARCH}.exe"
InstallDir "$PROGRAMFILES\Lite Agent CLI" ; Default installation directory
Unicode True ; Enable Unicode support for modern systems

; Pages
Page components
Page directory
Page instfiles
Page finish

; Uninstaller Name (used by Windows Add/Remove Programs)
UninstallText "This will uninstall Lite Agent CLI. Are you sure you want to continue?"
UninstallIcon "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Icon for the installer and the installed application
; Placeholder for a custom icon. For now, using default NSIS icon.
!define APP_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
Icon "${APP_ICON}"
UninstallIcon "${APP_ICON}"

; -------------------------------------------------------------------------------------------------------------------
; Sections
; -------------------------------------------------------------------------------------------------------------------

Section "Lite Agent CLI (Required)" SecApp
    SetOutPath "$INSTDIR" ; Set installation directory

    ; Copy the PyInstaller-bundled executable
    ; This path is relative to where makensis is run from, which will be host/windows/
    File "dist\esl-harness.exe"

    ; Create Uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Create Shortcuts
    CreateDirectory "$SMPROGRAMS\Lite Agent CLI"
    CreateShortcut "$SMPROGRAMS\Lite Agent CLI\Lite Agent CLI.lnk" "$INSTDIR\esl-harness.exe"
    CreateShortcut "$DESKTOP\Lite Agent CLI.lnk" "$INSTDIR\esl-harness.exe" "" "$INSTDIR\esl-harness.exe" 0

    ; Write uninstall information to the registry
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI" "DisplayName" "Lite Agent CLI"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI" "UninstallString" '"$INSTDIR\Uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI" "DisplayIcon" "$INSTDIR\esl-harness.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI" "Publisher" "Gemini Agent"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI" "HelpLink" "https://github.com/tanaynaidoo/Lite-Agent-Beta-Gemini-CLI-Harness-"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI" "NoRepair" 1

    ; Add to PATH (Optional - consider if the CLI needs to be globally accessible)
    ; This is a more advanced feature and requires careful thought about user experience
    ; and potential conflicts. For now, let's keep it simple.
    ; EnvVar /REPLACE "PATH" "$INSTDIR"

SectionEnd

; -------------------------------------------------------------------------------------------------------------------
; Uninstaller Section
; -------------------------------------------------------------------------------------------------------------------

Section "Uninstall"
    ; Delete files
    Delete "$INSTDIR\esl-harness.exe"
    Delete "$INSTDIR\Uninstall.exe"

    ; Delete Shortcuts
    Delete "$SMPROGRAMS\Lite Agent CLI\Lite Agent CLI.lnk"
    RMDir "$SMPROGRAMS\Lite Agent CLI"
    Delete "$DESKTOP\Lite Agent CLI.lnk"

    ; Delete registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Lite Agent CLI"

    ; Remove installation directory if empty
    RMDir "$INSTDIR"

    DetailPrint "Uninstallation complete."
SectionEnd