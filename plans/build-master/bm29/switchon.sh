# switchon.sh GAME.html : the Fable review's 21 switches on (TEX_READ_ON stays off). Fails unless each line is found once.
G=$1; bad=0
for s in LOOP_GUARD_ON SAVE_KEEP_ON SAVE_TELL_ON LIB_SAY_ON SLEEP_SAFE_ON LOAD_SAFE_ON EVON_MEMO_ON WALLS_STILL_ON SAVE_TAB_ON \
  FRP_LINE_ON FRP_FOOD_ON FRP_TRAY_ON FRP_PINTAP_ON FRP_LEAD_ON FRP_PANELS_ON FRP_LABEL_ON FRP_BLINK_ON FRP_THANKS_ON FRP_TIPS_ON FRP_SAY_ON FRP_WORDS_ON; do
  n=$(grep -c -E "^ *(const|var) $s = false;" $G); [ "$n" = 1 ] || { echo "PROBLEM $s: $n lines"; bad=1; continue; }
  sed -i -E "s/^( *(const|var) $s = )false;/\1true;/" $G
done
[ "$(grep -c -E '^const TEX_READ_ON = false;' $G)" = 1 ] || { echo "PROBLEM TEX_READ_ON is not off"; bad=1; }
echo "on: $(grep -c -E '^ *(const|var) (LOOP_GUARD|SAVE_KEEP|SAVE_TELL|LIB_SAY|SLEEP_SAFE|LOAD_SAFE|EVON_MEMO|WALLS_STILL|SAVE_TAB|FRP_[A-Z]+)_ON = true;' $G) of 21"; exit $bad
