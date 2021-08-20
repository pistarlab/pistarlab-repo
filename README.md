# piSTAR Lab Repo

Agent snapshot and extension repositories for [piSTAR Lab](http://github.com/pistarlab/pistarlab). 


## Extension Development Notes

We suggest using piSTAR Lab to create your extension.

- ids/spec_ids should be globaly unique within the the given entity type (agent_specs,environments,env_spec,task_specs,etc)
- the root project name should use hyphans "-" and no underscores "\_", while the packages name should have no hyphans "-" only underscores "\_". Otherwise they should share the same name and be prefixed with pistarlab

    Example of valid a project/package
    ```
    pistarlab-my-project/pistarlab_my_project
    ```
- a pistarlab_extension.json metadata file is required inside your python packages
- see an existing extension for more details.

## Local Testing
TODO

## Deploying Extensions to Repo

### Using script
run 
```
python scripts/update_extension_repo.py  --repo_index REPO_FILE_PATH
```

### Manually

Requirements: pistarlab should be installed

1. Navigate to extension source 
    ```
    cd src/EXTENSION_NAME/
    ```
1. Build manifest (only needed if extension requires a manifest)
    ```bash
    pistarlab_extension_tools --action=save_manifest --extension_path FULL_PATH_TO_EXTENSION_SOURCE
     ```
     Note: xvfb-run required if running remotely
1. Build Extension

    ```bash
    rm -rf build dist && python setup.py sdist bdist_wheel && unzip -l dist/*.whl
    ```
1. Move Distribution packages to ```extensions``` directory

    ```
    cp dist/* pistarlab-repo/extensions/repo
    ```

1. Update repo index under extensions/PISTARLAB_VERSION.json.

    1. open ```extensions/PISTARLAB_VERSION.json``` and insert (replace if entry for this extension exists) text JSON text from ```src/EXTENSION_NAME/pistarlab_extension.json```.

    1. add the key ```"type" :"rpath+whl"``` to the new entry
    
        Example of an updated entry in the repo index
        ```JSON
        {
            "id": "EXTENSION_ID",
            "version": ...,
            "name": ...,
            "categories": [
                ...
            ],
            "description": ...,
            "extension_author": ...,
            "original_author": ...,
            "type" :"rpath+whl"
        },

        ```

