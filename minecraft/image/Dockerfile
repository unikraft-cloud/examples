FROM itzg/minecraft-server:latest

COPY env.txt /env.txt

# Uncomment below if you want to use a custom world
# COPY --chown=minecraft:minecraft world/ /worlds/world/

COPY --chown=minecraft:minecraft --chmod=755 wrapper.sh /wrapper.sh
