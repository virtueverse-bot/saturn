# Use the Railway nix builder image
FROM railwayapp/builder:latest AS builder

# Set the working directory
WORKDIR /app

# Copy the nix files
COPY shell.nix ./

# Build the dependencies using nix
RUN nix-shell --run true

# Copy the rest of the application code
COPY . .

# Build the application
RUN nix-shell --run "chmod +x start.sh"
CMD ["./start.sh"]
