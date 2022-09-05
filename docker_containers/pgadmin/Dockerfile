FROM dpage/pgadmin4

USER pgadmin

COPY ./pgadmin/ /var/lib/pgadmin/

USER root

RUN chown 5050:5050 /var/lib/pgadmin/pgpass
RUN chmod 0600 /var/lib/pgadmin/pgpass

USER pgadmin

ENTRYPOINT ["/entrypoint.sh"]