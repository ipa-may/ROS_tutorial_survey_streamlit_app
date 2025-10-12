#!/usr/bin/env bash
set -euo pipefail

ALIASES_FILE="${HOME}/.bash_aliases"
BASHRC_FILE="${HOME}/.bashrc"

cat <<'EOF' > "${ALIASES_FILE}"
# Custom aliases for the python_streamlit dev container
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

alias alert="notify-send --urgency=low -i \"\$( [ \$? = 0 ] && echo terminal || echo error )\" \"\$(history | tail -n1 | sed -e 's/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//')\""
EOF

# Ensure .bashrc sources .bash_aliases exactly once.
if [ -f "${BASHRC_FILE}" ] && ! grep -Fq ".bash_aliases" "${BASHRC_FILE}"; then
    cat <<'EOF' >> "${BASHRC_FILE}"

# Load custom aliases if available
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
EOF
fi
