FROM postgres:12

# RUN /etc/init.d/postgresql start && \
#     psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';"

RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf

RUN echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf

EXPOSE 5432

CMD [ "postgres" ]

# ENV POSTGRES_USER docker
# ENV POSTGRES_PASSWORD docker
# ENV POSTGRES_DB eod_db
# ENV PG_TRUST_LOCALNET=true