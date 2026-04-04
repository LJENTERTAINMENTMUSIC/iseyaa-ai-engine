#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../iseyaa-web-core"
npm install
npm run dev
