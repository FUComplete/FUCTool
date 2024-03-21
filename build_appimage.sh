#!/usr/bin/env bash

name=fuctool-build
cmd=podman

$cmd build -t "$name" -f AppImage/Containerfile .
id=$($cmd create "$name")
$cmd cp "$id:/out/FUCTool-x86_64.AppImage" .
$cmd rm "$id"
