docker run --tmpfs /judger/run:exec \
    --tmpfs /judger/spj:exec \
    --tmpfs /log \
    --tmpfs /tmp \
    --rm --read-only --cap-drop FSETID \
    --cap-drop MKNOD \
    --cap-drop SETFCAP \
    --cap-drop SETPCAP \
    --cap-drop NET_BIND_SERVICE \
    --cap-drop SYS_CHROOT \
    judger_test /bin/bash -c "python3 test.py"
