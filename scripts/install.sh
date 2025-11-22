#!/bin/bash
# Claude Code Configuration Installer
# Automated setup and validation for Claude Code global configuration

set -euo pipefail

# Determine script directory and Claude config directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

# Source common library if available
if [ -f "$SCRIPT_DIR/scripts/lib/common.sh" ]; then
    source "$SCRIPT_DIR/scripts/lib/common.sh"
else
    # Minimal color support if common.sh not available
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
    log_info() { echo -e "${BLUE}ℹ${NC}  $*"; }
    log_success() { echo -e "${GREEN}✓${NC}  $*"; }
    log_warn() { echo -e "${YELLOW}⚠${NC}  $*"; }
    log_error() { echo -e "${RED}✗${NC}  $*"; }
    die() { log_error "$1"; exit "${2:-1}"; }
fi

# ============================================================================
# Configuration
# ============================================================================

INSTALL_MODE="${1:-full}"  # full, minimal, validate-only
SKIP_DEPS="${SKIP_DEPS:-0}"
SKIP_MCP="${SKIP_MCP:-0}"

# ============================================================================
# Functions
# ============================================================================

print_banner() {
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        Claude Code Global Configuration Installer            ║
║                                                               ║
║  Automated setup for Claude Code development environment     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo ""
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    local missing=()

    # Required commands
    local required=("git" "bash")
    for cmd in "${required[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing+=("$cmd")
        fi
    done

    # Optional but recommended commands
    local recommended=("jq" "node" "npm" "python3" "poetry")
    local missing_recommended=()
    for cmd in "${recommended[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            missing_recommended+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing required commands: ${missing[*]}"
        return 1
    fi

    if [ ${#missing_recommended[@]} -gt 0 ]; then
        log_warn "Missing recommended commands: ${missing_recommended[*]}"
        log_warn "Some features may not work without these"
    else
        log_success "All recommended tools available"
    fi

    return 0
}

create_directory_structure() {
    log_info "Creating directory structure..."

    local dirs=(
        "$CLAUDE_CONFIG_DIR/logs"
        "$CLAUDE_CONFIG_DIR/scripts/lib"
        "$CLAUDE_CONFIG_DIR/tmp_cleanup"
        "$CLAUDE_CONFIG_DIR/agents"
        "$CLAUDE_CONFIG_DIR/commands"
        "$CLAUDE_CONFIG_DIR/docs"
        "$CLAUDE_CONFIG_DIR/mcp"
        "$CLAUDE_CONFIG_DIR/standards"
        "$CLAUDE_CONFIG_DIR/templates"
    )

    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            log_success "Created: $dir"
        else
            log_info "Already exists: $dir"
        fi
    done
}

create_env_files() {
    log_info "Creating environment files..."

    # Create .env.mcp example if it doesn't exist
    if [ ! -f "$CLAUDE_CONFIG_DIR/.env.mcp.example" ]; then
        cat > "$CLAUDE_CONFIG_DIR/.env.mcp.example" << 'EOF'
# Claude MCP Environment Configuration
# Copy this file to .env.mcp and customize for your environment

# Zen MCP Server
ZEN_MCP_SERVER_PATH="$HOME/.claude/mcp/zen-mcp-server.js"
ZEN_AGENTS_DIR="$HOME/.claude/agents"
ZEN_LOG_LEVEL="info"

# GitHub Integration (required for GitHub MCP server)
# Get token from: https://github.com/settings/tokens
GITHUB_TOKEN="ghp_your_token_here"

# Project Paths (customize as needed)
PROJECT_ROOT="$HOME/dev"

# MCP Server Configuration
CLAUDE_MCP_CONFIG="$HOME/.claude/mcp/zen-server.json"
EOF
        log_success "Created: .env.mcp.example"
    fi

    # Prompt user to create .env.mcp if it doesn't exist
    if [ ! -f "$CLAUDE_CONFIG_DIR/.env.mcp" ]; then
        log_warn ".env.mcp not found"
        read -p "Create .env.mcp from example? [y/N] " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp "$CLAUDE_CONFIG_DIR/.env.mcp.example" "$CLAUDE_CONFIG_DIR/.env.mcp"
            log_success "Created: .env.mcp"
            log_warn "Please edit .env.mcp and add your GitHub token"
        else
            log_warn "Skipped .env.mcp creation - you'll need to create it manually"
        fi
    else
        log_info ".env.mcp already exists"
    fi
}

install_node_dependencies() {
    if [ "$SKIP_DEPS" = "1" ]; then
        log_info "Skipping Node.js dependency installation"
        return 0
    fi

    log_info "Checking Node.js dependencies..."

    if ! command -v npm &> /dev/null; then
        log_warn "npm not available, skipping Node.js dependencies"
        return 0
    fi

    # Check if npx works
    if npx --version &> /dev/null; then
        log_success "npx available (version: $(npx --version))"
    else
        log_error "npx not working properly"
        return 1
    fi
}

setup_git_config() {
    log_info "Configuring Git..."

    # Check if git signing is configured
    local signing_key=$(git config --get user.signingkey 2>/dev/null || echo "")

    if [ -z "$signing_key" ]; then
        log_warn "Git signing key not configured"
        log_info "To enable signed commits, run:"
        echo "  git config --global user.signingkey YOUR_GPG_KEY_ID"
        echo "  git config --global commit.gpgsign true"
    else
        log_success "Git signing configured (key: ${signing_key:0:16}...)"
    fi

    # Check GPG keys
    if command -v gpg &> /dev/null; then
        local gpg_keys=$(gpg --list-secret-keys --keyid-format LONG 2>/dev/null | grep -c "^sec" || echo "0")
        if [ "$gpg_keys" -gt 0 ]; then
            log_success "GPG keys found ($gpg_keys)"
        else
            log_warn "No GPG keys found - generate one with: gpg --gen-key"
        fi
    else
        log_warn "GPG not available"
    fi

    # Check SSH keys
    if command -v ssh-add &> /dev/null; then
        local ssh_keys=$(ssh-add -l 2>/dev/null | grep -v "no identities" | wc -l || echo "0")
        if [ "$ssh_keys" -gt 0 ]; then
            log_success "SSH keys loaded ($ssh_keys)"
        else
            log_warn "No SSH keys loaded - add with: ssh-add ~/.ssh/id_ed25519"
        fi
    fi
}

make_scripts_executable() {
    log_info "Making scripts executable..."

    if [ -d "$CLAUDE_CONFIG_DIR/scripts" ]; then
        find "$CLAUDE_CONFIG_DIR/scripts" -type f -name "*.sh" -exec chmod +x {} \;
        log_success "Scripts are now executable"
    fi
}

validate_configuration() {
    log_info "Validating configuration..."
    local validation_failed=0

    # Check settings.json
    if [ -f "$CLAUDE_CONFIG_DIR/settings.json" ]; then
        if command -v jq &> /dev/null; then
            if jq empty "$CLAUDE_CONFIG_DIR/settings.json" 2>/dev/null; then
                log_success "settings.json is valid"
            else
                log_error "settings.json is invalid JSON"
                validation_failed=1
            fi
        else
            log_warn "Cannot validate settings.json (jq not available)"
        fi
    else
        log_warn "settings.json not found"
    fi

    # Check MCP configuration
    if [ -f "$CLAUDE_CONFIG_DIR/mcp/zen-server.json" ]; then
        if command -v jq &> /dev/null; then
            if jq empty "$CLAUDE_CONFIG_DIR/mcp/zen-server.json" 2>/dev/null; then
                log_success "zen-server.json is valid"

                # Count configured servers
                local server_count=$(jq '.mcpServers | length' "$CLAUDE_CONFIG_DIR/mcp/zen-server.json")
                log_info "MCP servers configured: $server_count"
            else
                log_error "zen-server.json is invalid JSON"
                validation_failed=1
            fi
        fi
    else
        log_warn "zen-server.json not found"
    fi

    # Check CLAUDE.md
    if [ -f "$CLAUDE_CONFIG_DIR/CLAUDE.md" ]; then
        log_success "CLAUDE.md found"
    else
        log_error "CLAUDE.md not found - this is required!"
        validation_failed=1
    fi

    return $validation_failed
}

run_health_checks() {
    log_info "Running health checks..."

    # Check disk usage
    local disk_usage=$(du -sh "$CLAUDE_CONFIG_DIR" 2>/dev/null | cut -f1 || echo "unknown")
    log_info "Config directory size: $disk_usage"

    # Count files
    local file_count=$(find "$CLAUDE_CONFIG_DIR" -type f | wc -l)
    log_info "Total files: $file_count"

    # Check for large files
    local large_files=$(find "$CLAUDE_CONFIG_DIR" -type f -size +1M 2>/dev/null | wc -l)
    if [ "$large_files" -gt 0 ]; then
        log_warn "Found $large_files files larger than 1MB"
    fi
}

print_summary() {
    local install_status="$1"

    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    if [ "$install_status" = "success" ]; then
        echo -e "${GREEN}✓ Installation Complete${NC}"
    else
        echo -e "${YELLOW}⚠ Installation Complete with Warnings${NC}"
    fi
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "Next Steps:"
    echo ""
    echo "1. Edit your environment file:"
    echo "   \$ vim $CLAUDE_CONFIG_DIR/.env.mcp"
    echo ""
    echo "2. Add your GitHub token (required for GitHub MCP server)"
    echo "   Get token from: https://github.com/settings/tokens"
    echo ""
    echo "3. Configure Git signing (recommended):"
    echo "   \$ git config --global user.signingkey YOUR_GPG_KEY_ID"
    echo "   \$ git config --global commit.gpgsign true"
    echo ""
    echo "4. Test your configuration:"
    echo "   \$ $CLAUDE_CONFIG_DIR/scripts/validate-mcp-env.sh"
    echo ""
    echo "5. Start using Claude Code with your global configuration!"
    echo ""
    echo "Documentation:"
    echo "  - Global Standards: $CLAUDE_CONFIG_DIR/CLAUDE.md"
    echo "  - MCP Setup: $CLAUDE_CONFIG_DIR/mcp/README.md"
    echo "  - Organization Guide: $CLAUDE_CONFIG_DIR/PROJECT-ORGANIZATION-GUIDE.md"
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
}

show_usage() {
    cat << EOF
Usage: $0 [MODE]

Modes:
  full          Full installation (default)
  minimal       Minimal setup without optional dependencies
  validate-only Only validate existing configuration

Environment Variables:
  SKIP_DEPS=1   Skip dependency installation
  SKIP_MCP=1    Skip MCP server setup

Examples:
  $0                    # Full installation
  $0 minimal            # Minimal installation
  $0 validate-only      # Just validate
  SKIP_DEPS=1 $0        # Skip dependency checks

EOF
}

# ============================================================================
# Main Installation
# ============================================================================

main() {
    # Parse arguments
    case "${1:-}" in
        -h|--help|help)
            show_usage
            exit 0
            ;;
        validate-only)
            INSTALL_MODE="validate-only"
            ;;
        minimal)
            INSTALL_MODE="minimal"
            SKIP_DEPS=1
            ;;
        full|"")
            INSTALL_MODE="full"
            ;;
        *)
            log_error "Unknown mode: $1"
            show_usage
            exit 1
            ;;
    esac

    print_banner

    log_info "Installation mode: $INSTALL_MODE"
    log_info "Claude config directory: $CLAUDE_CONFIG_DIR"
    echo ""

    # Track installation status
    local install_status="success"

    # Validation-only mode
    if [ "$INSTALL_MODE" = "validate-only" ]; then
        validate_configuration || install_status="warning"
        run_health_checks
        print_summary "$install_status"
        exit 0
    fi

    # Full installation steps
    check_prerequisites || die "Prerequisites check failed"
    create_directory_structure
    create_env_files

    if [ "$INSTALL_MODE" = "full" ]; then
        install_node_dependencies || install_status="warning"
    fi

    setup_git_config
    make_scripts_executable
    validate_configuration || install_status="warning"
    run_health_checks
    print_summary "$install_status"

    # Return success even with warnings
    exit 0
}

# Run main function
main "$@"
