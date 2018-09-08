#!/bin/sh

ROOT=/opt
PROG_NAME=ebot
PROG_EXEC=ebot.py

PROG_PATH=$ROOT/$PROG_NAME
PROG_EXEC="$PROG_PATH/venv/bin/python $PROG_PATH/$PROG_EXEC"
PROG_PID=$PROG_PATH/$PROG_NAME.pid
PROG_LOG=$PROG_PATH/$PROG_NAME.log
PROG_ARGS="run --config production"

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/12.1/client64/lib

case $1 in
  start)
    echo "Starting $PROG_NAME ..."
    if [ ! -f $PROG_PID ]; then
      nohup $PROG_EXEC $PROG_ARGS >>$PROG_LOG 2>&1&
      echo $! > $PROG_PID
      echo "$PROG_NAME started ..."
    else
      echo "$PROG_NAME is already running ..."
    fi
  ;;
  stop)
    if [ -f $PROG_PID ]; then
      PID=$(cat $PROG_PID);
      echo "$PROG_NAME stoping ..."
      kill $PID;
      echo "$PROG_NAME stopped ..."
      rm $PROG_PID
    else
      echo "$PROG_NAME is not running ..."
    fi
  ;;
  restart)
    if [ -f $PROG_PID ]; then
      PID=$(cat $PROG_PID);
      echo "$PROG_NAME stopping ...";
      kill $PID;
      echo "$PROG_NAME stopped ...";
      rm $PROG_PID
      echo "$PROG_NAME starting ..."
      nohup $PROG_EXEC $PROG_ARGS >>$PROG_LOG 2>&1&
      echo $! > $PROG_PID
      echo "$PROG_NAME started ..."
    else
      echo "$PROG_NAME is not running ..."
    fi
  ;; esac
