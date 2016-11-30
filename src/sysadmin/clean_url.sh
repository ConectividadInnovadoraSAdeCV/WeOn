
LOG_PATH=$1
FILE=$2
YESTERDAY=`date +"%Y-%m-%d" -d "yesterday"`
echo $FILE

cp  "${LOG_PATH}/squid.log" "${LOG_PATH}/squid.log.${YESTERDAY}"

cat "${LOG_PATH}/squid.log" | \
    perl -p -e 's/ (..\/...\/.....(.*) .*)/ \2/g' | \
    sed 's/ / \| /g' |  \
    grep -Pv '.*(\.(jpg|js|css|gif|png|ico|php|woff|ttf|xml|swf|\w+\?)|\/((css|csi|js|fonts)[\/\?])|\w+\?|[\w\W]{200,}|\/(\?|jstag)|advert|[\;\:].*\=)' \
    | perl -p -e 's/ ((http:\/\/.+?\/)\w.*) / \2 | /g' | sort | uniq > "${LOG_PATH}/${FILE}"

echo "" > "${LOG_PATH}/squid.log"
