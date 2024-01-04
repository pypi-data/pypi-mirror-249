
# osjupyter Extension Deployment

## Introduction
This README provides instructions for deploying the `osjupyter` nbextension in a Jupyter environment. It outlines the necessary steps to install, enable, disable, and uninstall the extension, ensuring a smooth setup and deployment process.

## Prerequisites
- Jupyter Notebook must be installed in your environment.
- The `osjupyter` extension should be available in your environment.

## Initial Setup
Before deploying the `osjupyter` extension, it's essential to set up the environment properly. Run the following command to install all the required dependencies:

```bash
npm install
```

## Deployment Instructions
To deploy the `osjupyter` nbextension, follow these steps:

1. **Uninstall the existing `osjupyter` extension**:
   Removes any existing installation of the `osjupyter` nbextension.
   ```bash
   jupyter nbextension uninstall osjupyter
   ```

2. **Disable the `osjupyter` extension**:
   Disables the extension to reset any previous configurations.
   ```bash
   jupyter nbextension disable osjupyter/main
   ```

3. **Enable the `osjupyter` extension**:
   Re-enables the `osjupyter` extension.
   ```bash
   jupyter nbextension enable osjupyter/main
   ```

4. **Install the `osjupyter` extension**:
   Installs the `osjupyter` nbextension in your Jupyter environment.
   ```bash
   jupyter nbextension install osjupyter
   ```

## Deploying Code Changes
To deploy changes to the `osjupyter` extension code, use the following npm script:

```bash
npm run deploy
```

This command ensures that any updates or modifications to the extension are applied and active in your Jupyter environment.

## Conclusion
After following these instructions, the `osjupyter` nbextension should be successfully deployed and ready for use in your Jupyter environment. Verify the installation through the nbextensions list in your Jupyter notebook settings.
