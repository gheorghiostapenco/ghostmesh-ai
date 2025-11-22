terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = ">= 4.0.0"
    }
  }
}

# 1. Provider Setup (Authentication)
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# 2. Networking (VCN & Subnet) - Required for the server to talk to the internet
resource "oci_core_vcn" "free_vcn" {
  cidr_block     = "10.0.0.0/16"
  compartment_id = var.tenancy_ocid
  display_name   = "free-tier-network"
  dns_label      = "freevcn"
}

resource "oci_core_internet_gateway" "free_ig" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_vcn.free_vcn.id
  display_name   = "free-gateway"
  enabled        = true
}

resource "oci_core_route_table" "free_rt" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_vcn.free_vcn.id
  display_name   = "free-route-table"

  route_rules {
    destination       = "0.0.0.0/0"
    destination_type  = "CIDR_BLOCK"
    network_entity_id = oci_core_internet_gateway.free_ig.id
  }
}

resource "oci_core_subnet" "free_subnet" {
  cidr_block        = "10.0.1.0/24"
  compartment_id    = var.tenancy_ocid
  vcn_id            = oci_core_vcn.free_vcn.id
  display_name      = "free-subnet"
  route_table_id    = oci_core_route_table.free_rt.id
  security_list_ids = [oci_core_security_list.free_security_list.id]
}

# 3. Firewall Rules (Security List) - Allow SSH (22) and Web (80/443)
resource "oci_core_security_list" "free_security_list" {
  compartment_id = var.tenancy_ocid
  vcn_id         = oci_core_vcn.free_vcn.id
  display_name   = "allow_ssh_http"

  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
  }

  ingress_security_rules {
    protocol = "6" # TCP
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22
    }
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 80
      max = 80
    }
  }
}

# 4. Dynamic Image Lookup (Find the latest Ubuntu ARM Image)
data "oci_core_images" "ubuntu_arm" {
  compartment_id   = var.tenancy_ocid
  operating_system = "Canonical Ubuntu"
  operating_system_version = "22.04"
  shape            = "VM.Standard.A1.Flex"
  sort_by          = "TIMECREATED"
  sort_order       = "DESC"
}

# 5. The "Monster" Server (4 OCPU / 24GB RAM)
resource "oci_core_instance" "free_instance" {
  availability_domain = data.oci_identity_availability_domain.ad.name
  compartment_id      = var.tenancy_ocid
  display_name        = "AlwaysFree-Server"
  shape               = "VM.Standard.A1.Flex"

  shape_config {
    ocpus         = 4
    memory_in_gbs = 24
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.free_subnet.id
    assign_public_ip = true
  }

  source_details {
    source_type = "image"
    source_id   = data.oci_core_images.ubuntu_arm.images[0].id
  }

  metadata = {
    ssh_authorized_keys = file(var.ssh_public_key_path)
  }
}

# Data source to get Availability Domain (AD)
data "oci_identity_availability_domain" "ad" {
  compartment_id = var.tenancy_ocid
  ad_number      = 2 # Change to 2 or 3 if AD-1 is full
}

output "server_public_ip" {
  value = oci_core_instance.free_instance.public_ip
}