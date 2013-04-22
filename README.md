# puppet-ovh

## Overview

This module manages configuration specific to OVH. See http://www.ovh.com/ for
more details.

* `ovh::oco::check` : Manage OvhCheckOut checks
* `ovh::oco::sshkey` : Manage the OVH support team SSH key's presence

To cleanly install the OCO daemon on Red Hat Enterprise Linux, you will find
the source, the spec and an init script under the `oco-rpm` directory.

## Examples

Enable the original ssh key-based root access for OVH's support staff (which
is restricted by IP address) :

    ovh::sshkey { 'root': }

Revoke the access, useful if it was just temporarily for diagnostics :

    ovh::sshkey { 'root': ensure => absent }

Enable a local OCO check on the node (this will automatically include the
daemon) :

    ovh::oco::check { 'http':
      freq      => '300sec',
      http_path => '/my-health-check.php',
    }

Disable the same OCO check :

    ovh::oco::check { 'http':
      freq      => '300sec',
      http_path => '/my-health-check.php',
      ensure    => absent,
    }

