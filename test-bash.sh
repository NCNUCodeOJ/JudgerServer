docker run -it -v $PWD:/code -v $PWD/testcase/case/:/test_case \
               --tmpfs /judger/run:exec \
               --tmpfs /judger/spj:exec \
               --tmpfs /log \
               --tmpfs /tmp \
               --rm  --read-only\
               --cap-drop SETPCAP \
               --cap-drop MKNOD \
               --cap-drop NET_BIND_SERVICE \
               --cap-drop SYS_CHROOT \
               --cap-drop SETFCAP \
               --cap-drop FSETID \
               judger_test /bin/bash