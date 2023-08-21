#!/bin/bash

docker compose up db -d
docker compose up db-isready -d
prisma db push