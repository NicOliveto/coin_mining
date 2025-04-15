FROM postgres:17.4
LABEL authors="nicolasoliveto"

# Script de inicializacion
COPY ./db/data/currency_data.sql /docker-entrypoint-initdb.d/

# Expongo el puerto de postgresql
EXPOSE 5432
