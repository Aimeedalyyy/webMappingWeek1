# Deployment Guide

## Prerequisites
- Ubuntu 20.04+ server
- Domain name pointing to your server
- SSH access to server

## Installation Steps

### 1. Server Setup
```bash
sudo apt update
sudo apt install nginx postgresql postgresql-contrib postgis
sudo systemctl enable nginx postgresql
