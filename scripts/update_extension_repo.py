import os

import subprocess
from pathlib import Path
import json
import argparse

def run_command(cmd,fail_ok=False):
    try:
        print(f"RUNNING CMD: {cmd}")
        command_output = subprocess.check_output(cmd,shell=True, text=True)
        print(f"OUTPUT: {command_output}")
    except Exception as e:
        if not fail_ok:
            raise e

def main(repo_path, skip_manifest_build=False):
    
    project_root = os.path.abspath(Path(__file__).parent.parent)

    repo_list=[]
    try:
        with open(repo_path,"r") as f:
            repo_list = json.load(f)
            repo = {f"{r['id']}--{r['version']}":r for r in repo_list}
    except Exception as e:
        print("Failed to load existing repo. Updating anyway")
        pass
        repo={}

    
    print(f"project_root: {project_root}")
    src_dir = os.path.join(project_root,"src")
    extension_names = os.listdir(src_dir)
    updated_count = 0
    count = 0
    successful_additions = []
    manifest_fails = []
    for ext_name in extension_names:
        print(ext_name)

        try:
            extension_src_path = os.path.join(src_dir,ext_name)#,project_name.replace("-","_"))
            if not os.path.exists(os.path.join(extension_src_path,ext_name.replace("-","_"),"extension_meta.json")):
                print(f"Skipping {ext_name} no extension_meta.json file")
                continue

            extension_package_name = ext_name.replace('-',"_")
            if not skip_manifest_build:
                try:
                    run_command(f"pistarlab_extension_tools --action=save_manifest --extension_path {extension_src_path}",fail_ok=False)
                except Exception as e:
                    manifest_fails.append(ext_name)
            run_command(f"cd {extension_src_path}; rm -rf build dist && python setup.py bdist_wheel && unzip -l dist/*.whl")
            run_command(f"cp {extension_src_path}/dist/* {project_root}/extensions/repo")
            with open(os.path.join(extension_src_path,extension_package_name,"extension_meta.json"),"r") as f:
                einfo = json.load(f)
            version = einfo['version']
            key = f"{einfo['id']}--{version}"
            path = f"repo/{extension_package_name}-{version}-py3-none-any.whl"
 
            einfo['type'] = "rpath+whl"
            einfo['path'] = path
            if key in repo:
                updated_count+=1
            repo[key] = einfo
            count +=1
            successful_additions.append(key)

        except Exception as e:
            # print(f"Failed to load {ext_name}")
            # print(e)
            # print()
            print()

    with open(repo_path,"w") as f:
        json.dump(list(repo.values()),f,indent=4)
    print(f"Updated repo at {repo_path}.  {updated_count} updated entries and {count-updated_count} new entries")
    print("")
    print(f"Extensioned processed successfully: {successful_additions}")
    print("")
    if not skip_manifest_build:
        print(f"Failed manifest runs for (this might be ok, depends on the extension): {manifest_fails}")


        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_index", required=True , help="Path to repo index")
    parser.add_argument("--skip_manifest_build",
                        action="store_true", help="Skip building manifest ")
    args = parser.parse_args()

    main(args.repo_index,args.skip_manifest_build)

