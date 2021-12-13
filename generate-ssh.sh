# Easy SSL generation
ROUTE_NAME=*.artifacts.developer.gov.bc.ca
ROUTE_ABRR=*_artifacts_developer_gov_bc_ca
DATE=$(date +%Y-%m-%d)
FULL=csr-${ROUTE_ABRR}-${DATE}
mkdir ${FULL} && cd ${FULL}
openssl req -new -newkey rsa:2048 -nodes \
  -out ${FULL}.csr \
  -keyout ${FULL}.key \
  -subj "/C=CA/ST=British Columbia/L=Victoria/O=Government of British Columbia/OU=Office of Chief Information Officer/CN=${ROUTE_NAME}"

