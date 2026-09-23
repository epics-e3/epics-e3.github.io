# Custom conda channels

For facilities that want to distribute internally developed E3 modules alongside a shared or central channel this can be achieved by running a custom conda repository solution.

## ESS shared channel

At ESS, the `ess-conda-local` channel on ESS Artifactory is a shared, centrally managed Conda channel containing:

- Officially released EPICS E3 modules
- Common dependencies and toolchains
- Packages validated for broad facility use

## Why operate your own conda channel?

Running your own Conda channel allows a facility to:

- Distribute EPICS E3 modules under its own release policy
- Control exactly which versions are available to IOCs and developers
- Isolate experimental, project-specific, or facility-local modules
- Ensure reproducible environments for commissioning and operations
- Integrate EPICS module delivery into CI/CD workflows

Many facilities maintain EPICS modules that:

- Are specific to local hardware or infrastructure
- Contain site-specific configuration or policies
- Are not intended for upstream or shared distribution

A private channel allows you to:

- Release and version these modules formally
- Treat them as production-quality packages
- Avoid pushing facility-specific content into shared channels

This is especially relevant when consuming shared channels such as `conda-forge`, while still needing local extensions.

Private channels help maintain clear boundaries:

- Shared channels
  - Generic, widely applicable modules
  - Maintained by a central group
- Private (facility or project) channels
  - Facility-specific modules
  - Local policies, naming, and release cadence

This separation reduces coupling between facilities and simplifies long-term maintenance.

## Conda repository solutions

Conda channels are served over HTTP(S), and multiple repository solutions can host them.
The choice depends on scale, governance, and operational constraints.

### Static HTTP / Object Storage

**Description**

- Conda channel stored as static files
- Served via:
  - Apache / NGINX
  - S3-compatible object storage
  - Network filesystems

**Pros**

- Simple and lightweight
- No database required
- Easy to back up

**Cons**

- Manual metadata generation (`conda index`)
- Limited access control
- Not ideal for frequent uploads or CI-driven workflows

**Typical Use**

- Small installations
- Archived or frozen repositories
- Offline environments

### JFrog Artifactory

**Description**

- Enterprise-grade artifact repository
- Native support for Conda repositories
- Often already deployed at large facilities (e.g. ESS)

**Pros**

- Automatic Conda metadata management
- Fine-grained access control
- High availability and backup support
- Multi-format support (Conda, RPM, PyPI, Docker, etc.)
- Well-supported CI/CD integrations

**Cons**

- Commercial licensing (beyond OSS edition)
- Heavier operational footprint

**Typical Use**

- Central or shared facility repositories
- Environments requiring strong governance
- Long-term production deployments

**Resources**
- [Webpage](https://jfrog.com/artifactory/)
- [Documentation](https://docs.jfrog.com/artifactory/docs)

### Quetz (mamba-org)

**Description**

- Open-source Conda repository server
- Developed by the mamba ecosystem
- Conda-focused design

**Pros**

- Fully open-source
- Automatic metadata handling
- Good performance with `mamba`
- Simple permission model per channel
- Lightweight compared to Artifactory

**Cons**

- Conda-only (no multi-format artifacts)
- Smaller operational ecosystem
- HA and backup require more manual setup

**Typical Use**

- Facility-local or project-local channels
- Open-source–oriented environments
- Facilities without an existing Artifactory deployment

**Resources**
- [GitHub project](https://github.com/mamba-org/quetz)
- [Documentation](https://quetz.readthedocs.io/)

### Summary comparison

| Feature | Static HTTP | Artifactory | Quetz |
|------|-------------|-------------|-------|
| Automatic metadata | ❌ | ✅ | ✅ |
| Access control | Limited | ✅ | ✅ |
| CI/CD friendly | ❌ | ✅ | ✅ |
| Open-source | ✅ | ❌ / partial | ✅ |
| Multi-format support | ❌ | ✅ | ❌ |
| Typical scale | Small | Medium–Large | Small–Medium |

### Channel client configuration

Private channels can override shared packages when required:

```bash
conda config --add channels facility-conda-local
conda config --add channels ess-conda-local
conda config --set channel_priority strict
```

This enables:

- Facility-specific variants of shared modules
- Local rebuilds with different compiler flags or dependencies
- Controlled divergence from shared releases

## Uploading and releasing packages in Artifactory (jfrog-cli)

```bash
jfrog rt upload \
  "conda-bld/linux-64/my-facility-module-2.0.0-0.tar.bz2" \
  facility-conda-local/linux-64/
```
## Uploading and releasing packages in Quetz

Upload to a facility-local channel:

```bash
quetz package upload facility-conda-local \
  "conda-bld/linux-64/my-facility-module-2.0.0-0.tar.bz2"
```

## Operational best practices

- Treat facility-private channels as first-class release channels
- Document which channels are authoritative for which modules
- Use strict channel priority everywhere
- Regularly review and audit channel usage
