# Chatudo public website. Static output only, no server-side code.
# Build step is offline (python3 build/render.py); this image just serves
# the already-generated public/ directory, so the image build never needs
# network access.
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY public/ /usr/share/nginx/html/

EXPOSE 80
