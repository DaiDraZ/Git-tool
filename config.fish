if status is-interactive
    set -Ua fish_features no-keyboard-protocols
    set -gx PATH $PATH $HOME/go/bin
    # Commands to run in interactive sessions can go here
end
