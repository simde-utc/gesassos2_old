while read -r line
do
cat > /etc/nginx/assos/${line}.conf <<EOF
location /${line}/ {
  #more_set_input_headers 'Host: ${line}.\$http_host';
  #rewrite      ^/${line}/(.*)$  /\$1  break;
  proxy_pass      http://web.mde.utc;
}
EOF
done < "/root/assos.list"
service nginx reload