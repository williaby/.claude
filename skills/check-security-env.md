# Security Environment Validation

**Purpose**: Validate security configuration for signed commits and encrypted secrets.

**Usage**: `/check-security-env` or `/check-security-env --verbose`

---

## Security Requirements Checklist

### 1. SSH Key Validation (Signed Commits)

```bash
# Check if SSH key is loaded
ssh-add -l
```

**Expected**:
- At least one SSH key loaded in ssh-agent
- Key should be 256-bit or higher (Ed25519, RSA 4096+)

**If fails**:
- Check if ssh-agent is running: `eval "$(ssh-agent -s)"`
- Load SSH key: `ssh-add ~/.ssh/id_ed25519` (or appropriate key)
- Verify key permissions: `chmod 600 ~/.ssh/id_ed25519`

### 2. Git Commit Signing Configuration

```bash
# Check global Git signing configuration
git config --global --get user.signingkey
git config --global --get commit.gpgsign
git config --global --get gpg.format

# Check local repository overrides
git config --local --get commit.gpgsign
git config --local --get user.signingkey
```

**Expected (SSH Signing)**:
```
gpg.format = ssh
commit.gpgsign = true
user.signingkey = ~/.ssh/id_ed25519.pub  (or appropriate public key)
```

**Expected (GPG Signing)**:
```
commit.gpgsign = true
user.signingkey = <GPG_KEY_ID>
```

**If fails**:
```bash
# For SSH signing (recommended)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# For GPG signing (alternative)
git config --global user.signingkey <YOUR_GPG_KEY_ID>
git config --global commit.gpgsign true
```

### 3. GPG Key Validation (Optional - for .env encryption)

```bash
# List GPG secret keys
gpg --list-secret-keys
```

**Expected** (if using encrypted secrets):
- At least one GPG key available
- Key should not be expired
- Key should have encryption capability

**If fails**:
```bash
# Generate new GPG key
gpg --full-generate-key

# Choose:
# - RSA and RSA (default)
# - 4096 bits
# - Does not expire (or appropriate duration)
```

### 4. Git User Configuration

```bash
# Verify user identity
git config --global --get user.name
git config --global --get user.email
```

**Expected**:
- user.name set to your name
- user.email set to your commit email

**If fails**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 5. Branch Protection Compliance

```bash
# Check if current branch allows force push
git config --get branch.$(git branch --show-current).pushRemote
git config --get remote.origin.url
```

**Expected**:
- Remote configured correctly
- No force push attempts on protected branches (main, develop)

### 6. Local Repository Safety

```bash
# Check for uncommitted changes
git status --porcelain

# Check for unsigned commits (last 10)
git log -10 --pretty=format:"%h %G? %s" | grep -v "^[a-f0-9]* G"
```

**Expected**:
- Clean working directory (or expected changes)
- Recent commits should be signed (%G? shows "G" for good signature)

**Signature Status Codes**:
- `G` = Good signature (valid)
- `B` = Bad signature (invalid)
- `U` = Good signature with unknown validity
- `X` = Good signature that has expired
- `Y` = Good signature made by expired key
- `R` = Good signature made by revoked key
- `E` = Cannot check signature
- `N` = No signature

---

## Output Format

```
🔐 Security Environment Validation

✅ SSH Key Configuration
   - Key loaded: Ed25519 SHA256:abc123... (2048-bit)
   - Key file: ~/.ssh/id_ed25519

✅ Git Signing Configuration
   - Signing enabled: true (SSH)
   - Signing key: ~/.ssh/id_ed25519.pub
   - Format: ssh

✅ GPG Configuration (Optional)
   - GPG key available: ABCD1234
   - Key type: RSA 4096-bit
   - Expiration: None

✅ Git User Configuration
   - Name: Byron Williams
   - Email: byron@example.com

✅ Repository Status
   - Remote: git@github.com:williaby/image-preprocessing-detector.git
   - Branch: feature/add-orientation-detection
   - Working directory: Clean

✅ Commit Signature Verification
   - Last 10 commits: All signed ✅
   - Signature type: SSH

---

🎯 Security Posture: SECURE ✅

Ready to commit with signed commits and encrypted secrets.
```

---

## Verbose Mode

When `--verbose` flag is provided, show additional details:

```
🔐 Security Environment Validation (Verbose)

SSH Key Details:
├─ Algorithm: Ed25519
├─ Fingerprint: SHA256:abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
├─ Comment: byron@laptop
├─ Added: 2024-11-06 12:34:56
└─ Agent PID: 12345

Git Global Configuration:
├─ user.name: Byron Williams
├─ user.email: byron@example.com
├─ commit.gpgsign: true
├─ gpg.format: ssh
├─ user.signingkey: $HOME/.ssh/id_ed25519.pub
└─ core.editor: vim

Git Local Configuration (Overrides):
└─ (none)

GPG Keys:
├─ Key ID: ABCD1234EFGH5678
├─ Type: RSA 4096
├─ Created: 2024-01-15
├─ Expires: Never
├─ User ID: Byron Williams <byron@example.com>
└─ Capabilities: Sign, Certify, Encrypt

Recent Commit Signatures:
├─ abc123d G feat: Add orientation detection
├─ def456e G fix: Update schema validation
├─ ghi789f G docs: Update README
├─ jkl012a G test: Add integration tests
└─ mno345b G chore: Update dependencies

Repository Safety:
├─ Protected branches: main, develop
├─ Current branch: feature/add-orientation-detection (unprotected)
├─ Uncommitted changes: 3 files modified
└─ Untracked files: 0
```

---

## Interactive Fix Mode

When issues are detected, offer to fix them:

```
❌ Git Signing Configuration

Issue: Signing not enabled
   git config --global commit.gpgsign: (not set)

💡 Fix Options:
1. Enable SSH signing (recommended)
   git config --global gpg.format ssh
   git config --global user.signingkey ~/.ssh/id_ed25519.pub
   git config --global commit.gpgsign true

2. Enable GPG signing
   git config --global user.signingkey <GPG_KEY_ID>
   git config --global commit.gpgsign true

3. Skip (not recommended for production)

Select option (1-3): _
```

---

## Warning Conditions

**⚠️ Warnings** (non-blocking):
- SSH key < 2048 bits (upgrade recommended)
- GPG key expiring within 30 days
- Unsigned commits found in last 10 commits
- Local git config overriding global signing settings

**❌ Errors** (blocking):
- No SSH key loaded in ssh-agent
- Commit signing disabled
- No git user.name or user.email configured
- Working on main/develop with uncommitted changes

---

## Security Best Practices

### SSH vs GPG Signing

**SSH Signing** (Recommended):
- ✅ Simpler setup (reuse existing SSH keys)
- ✅ No key expiration management
- ✅ Native GitHub support
- ✅ Faster than GPG

**GPG Signing** (Alternative):
- ✅ More widely supported
- ✅ Can encrypt files (.env, secrets)
- ⚠️ Requires key management
- ⚠️ Slower than SSH

### Branch Protection Workflow

1. **Protected branches** (main, develop):
   - Require signed commits
   - Require status checks (ci-gate, security-gate-success)
   - No force pushes
   - Linear history

2. **Feature branches**:
   - Signed commits recommended
   - Regular commits with descriptive messages
   - Squash or rebase before merging to protected branches

### Encrypted Secrets Management

If using GPG for .env encryption:

```bash
# Encrypt .env file
gpg --encrypt --recipient your.email@example.com .env

# Decrypt .env.gpg
gpg --decrypt .env.gpg > .env

# Add .env to .gitignore (never commit unencrypted secrets)
echo ".env" >> .gitignore
```

---

## Success Criteria

All checks pass:
- ✅ SSH key loaded in ssh-agent
- ✅ Git signing enabled (SSH or GPG)
- ✅ Signing key configured
- ✅ Git user identity configured
- ✅ Recent commits are signed
- ✅ No local overrides disabling signing
- ✅ (Optional) GPG key available for encryption

**Security Posture**: SECURE ✅

**Ready to commit**: All security requirements met
