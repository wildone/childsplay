
$HOSTADDRESS = Get-Content .\host.address -Raw

Write-Output "Starting Docker container to connect server:"
docker run -it --rm -v ${PWD}:/build/source:rw -v ${HOME}/.ssh:/build/.ssh:ro aemdesign/centos-java-buildpack bash --login /build/source/docker-connect.sh "${HOSTADDRESS}"
