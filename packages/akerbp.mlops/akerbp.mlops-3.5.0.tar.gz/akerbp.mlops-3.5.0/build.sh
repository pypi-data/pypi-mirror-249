# build.sh
#
# Package version number relies on git tags
# Building logic enables building in dev and then using the same version in test
# Setup.py reads tags to create the version label
if [ "$BITBUCKET_REPO_FULL_NAME" = "akerbp/mlops" ] || [ "$MODEL_ENV" = "dev" ]
echo "Build script for akerbp.mlops package"
then
    if [ "$MODEL_ENV" != "dev" ]
    then
        echo "Install build dependencies"
        pip install twine==4.0.2;
        pip install build==0.10.0;
    fi

    # Build and upload if new tag was applied (or prod)
    if [ "$MODEL_ENV" = "test" ] || [ "$MODEL_ENV" = "prod" ]
    then
        echo "Tag release"
        tag=$(python increment_package_version.py);
        commit=$(git rev-parse --short HEAD);
        echo "Deleting tag if it already exists: $tag"
        # Check if the tag exists before attempting to delete it
        if git rev-parse --quiet --verify refs/tags/$tag >/dev/null 2>&1; then
            echo "Tag $tag already exists, deleting"
            git tag -d $tag
            git push origin :refs/tags/$tag
        fi
        echo "Tagging commit with tag: $tag"
        git tag $tag $commit
        git push origin $tag
        echo "Build package"
        python -m build
        echo "Upload package"
        python -m twine upload \
            --disable-progress-bar \
            --non-interactive \
            dist/*
    else
        echo "Won't build and upload!"
    fi
    if [ "$MODEL_ENV" = "dev" ]
    then
        echo "Clean up!"
        rm -fR build/ dist/ src/akerbp.mlops.egg-info/
    fi
fi
