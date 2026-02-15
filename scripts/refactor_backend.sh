#!/bin/bash
set -e

echo "Starting Backend Refactoring..."

# 1. Rename directories (safe check)
# Only rename if the hyphenated directory exists
[ -d "libs/core-kernel" ] && mv libs/core-kernel libs/core_kernel && echo "Renamed core-kernel -> core_kernel" || echo "core-kernel not found or already renamed"
[ -d "libs/infra-db" ] && mv libs/infra-db libs/infra_db && echo "Renamed infra-db -> infra_db" || echo "infra-db not found or already renamed"
[ -d "libs/infra-net" ] && mv libs/infra-net libs/infra_net && echo "Renamed infra-net -> infra_net" || echo "infra-net not found or already renamed"

# 2. Move Telemetry (if not already moved)
mkdir -p libs/telemetry
if [ -f "libs/core_kernel/telemetry.py" ]; then
    mv libs/core_kernel/telemetry.py libs/telemetry/__init__.py
    echo "Moved telemetry.py to libs/telemetry/__init__.py"
else
    echo "libs/core_kernel/telemetry.py not found (already moved?)"
fi

# 3. Update Imports (Using sed)
# Config for explicit python import updates
# Note: macOS sed requires empty string for -i backup extension
echo "Updating imports in apps/ and libs/..."

# Helper function to run replacement
replace_imports() {
    local search="$1"
    local replace="$2"
    echo "Replacing '$search' with '$replace'..."
    find apps libs -name "*.py" -type f -exec sed -i '' "s/$search/$replace/g" {} +
}

replace_imports "from libs.core-kernel" "from libs.core_kernel"
replace_imports "from libs.infra-db" "from libs.infra_db"
replace_imports "from libs.infra-net" "from libs.infra_net"
replace_imports "from libs.core_kernel.telemetry" "from libs.telemetry"
# Catch underscore variants too just in case
replace_imports "from libs.core_kernel.telemetry" "from libs.telemetry"

echo "Refactoring Complete."
