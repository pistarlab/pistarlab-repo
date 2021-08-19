# piSTAR Lab Repo

This is the main repository for [piSTAR Lab](http://github.com/pistarlab/pistarlab). 




## Deploying Extensions to Repo

1. Navigate to extension source 
    ```
    cd src/EXTENSION_NAME/
    ```
1. Build manifest (only needed if extension requires a manifest)
    ```
    pistarlab_extension_tools --action=save_manifest --extension_path FULL_PATH_TO_EXTENSION_SOURCE
     ```
     Note: xvfb-run required if running remotely
1. Build Extension

    ```
    rm -rf build dist && python setup.py sdist bdist_wheel && unzip -l dist/*.whl
    ```
1. Move Distribution packages to ```extensions``` directory

    ```
    cp dist/* pistarlab-repo/extensions/repo
    ```

1. Update repo index under 

