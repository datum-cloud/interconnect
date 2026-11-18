#!/usr/bin/env python3
"""
Generate Draw.io architecture diagrams for Datum's Interconnect Offering.
Produces a multi-page .drawio file and individual diagrams for each view:
1. Ecosystem & Virtual Meet-Me Room (vMMR)
2. Technical Architecture & Protocol Stack
3. Concrete Practical Deployment & Packet Flow
4. Dynamic Tunnel & Datum Connect Agent Lifecycle
"""

import os
import sys
import xml.etree.ElementTree as ET

class DrawioDiagramBuilder:
    def __init__(self, name, page_width=1920, page_height=1200, bg="#0F172A"):
        self.name = name
        self.page_width = page_width
        self.page_height = page_height
        self.bg = bg
        self.cell_id = 2
        self.cells = []

    def next_id(self):
        cid = str(self.cell_id)
        self.cell_id += 1
        return cid

    def add_box(self, label, x, y, w, h, style_dict=None):
        cid = self.next_id()
        default_style = {
            "rounded": "1",
            "whiteSpace": "wrap",
            "html": "1",
            "arcSize": "10",
        }
        if style_dict:
            default_style.update(style_dict)
        style_str = ";".join(f"{k}={v}" for k, v in default_style.items()) + ";"
        self.cells.append({
            "id": cid,
            "value": label,
            "style": style_str,
            "vertex": "1",
            "x": x, "y": y, "w": w, "h": h
        })
        return cid

    def add_edge(self, source_id, target_id, label="", style_dict=None):
        cid = self.next_id()
        default_style = {
            "edgeStyle": "orthogonalEdgeStyle",
            "rounded": "1",
            "orthogonalLoop": "1",
            "jettySize": "auto",
            "html": "1",
            "strokeColor": "#38BDF8",
            "strokeWidth": "2",
            "fontColor": "#E2E8F0",
            "fontSize": "11",
        }
        if style_dict:
            default_style.update(style_dict)
        style_str = ";".join(f"{k}={v}" for k, v in default_style.items()) + ";"
        self.cells.append({
            "id": cid,
            "value": label,
            "style": style_str,
            "edge": "1",
            "source": source_id,
            "target": target_id
        })
        return cid

    def to_xml(self, diagram_id="diagram"):
        root = ET.Element("diagram", {"id": diagram_id, "name": self.name})
        model = ET.SubElement(root, "mxGraphModel", {
            "dx": "1600", "dy": "1000", "grid": "1", "gridSize": "10",
            "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
            "fold": "1", "page": "1", "pageScale": "1",
            "pageWidth": str(self.page_width), "pageHeight": str(self.page_height),
            "background": self.bg, "math": "0", "shadow": "0"
        })
        mroot = ET.SubElement(model, "root")
        ET.SubElement(mroot, "mxCell", {"id": "0"})
        ET.SubElement(mroot, "mxCell", {"id": "1", "parent": "0"})

        for c in self.cells:
            attribs = {"id": c["id"], "value": c["value"], "style": c["style"], "parent": "1"}
            if c.get("vertex") == "1":
                attribs["vertex"] = "1"
                cell = ET.SubElement(mroot, "mxCell", attribs)
                ET.SubElement(cell, "mxGeometry", {
                    "x": str(c["x"]), "y": str(c["y"]), "width": str(c["w"]), "height": str(c["h"]), "as": "geometry"
                })
            elif c.get("edge") == "1":
                attribs["edge"] = "1"
                attribs["source"] = c["source"]
                attribs["target"] = c["target"]
                cell = ET.SubElement(mroot, "mxCell", attribs)
                ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})

        return root

# --- Build Diagram 1: Ecosystem Overview (The Virtual Meet-Me Room) ---
def build_diagram_1():
    b = DrawioDiagramBuilder("1. Ecosystem Overview - Virtual Meet-Me Room", 1920, 1150)
    
    # Header Banner
    b.add_box(
        "<b><font size='5' color='#F8FAFC'>DATUM INTERCONNECT: THE NEUTRAL VIRTUAL MEET-ME ROOM (vMMR)</font></b><br/><font color='#94A3B8' size='3'>Unified Private &amp; Public Transit across Neoclouds, Hyperscalers, and Last-Mile Providers via Dynamic Tunnels</font>",
        40, 30, 1840, 70,
        {"fillColor": "#1E293B", "strokeColor": "#334155", "fontColor": "#FFFFFF", "align": "center"}
    )

    # 1. Neoclouds Box (Top-Left)
    neo_bg = b.add_box(
        "<b><font size='3' color='#DDD6FE'>NEOCLOUDS &amp; AI COMPUTE CLOUDS</font></b><br/><font color='#A78BFA' size='2'>High-Density GPU Clusters • Foundation Model Training • Inference Engines</font>",
        50, 130, 480, 440,
        {"fillColor": "#2E1065", "strokeColor": "#8B5CF6", "strokeWidth": "2", "verticalAlign": "top", "align": "center", "opacity": "90"}
    )
    b.add_box(
        "<b>CoreWeave / Lambda / Nebius / Together AI</b><br/><font color='#C4B5FD'>• 10k+ GPU Clusters (H100/B200)<br/>• Fast RoCEv2 / InfiniBand Fabric<br/>• Rapid compute scaling<br/><b>Challenge:</b> Siloed network, steep egress fees, no native private path to enterprise data.</font>",
        70, 200, 440, 100,
        {"fillColor": "#3B0764", "strokeColor": "#7C3AED", "fontColor": "#EDE9FE", "align": "left"}
    )
    b.add_box(
        "<b>Workloads &amp; Endpoints</b><br/><font color='#C4B5FD'>• Distributed PyTorch / vLLM workers<br/>• Checkpoint streaming pipelines<br/>• Model serving APIs<br/>• Internal RFC 4193 ULA / Private IPs</font>",
        70, 320, 440, 95,
        {"fillColor": "#3B0764", "strokeColor": "#7C3AED", "fontColor": "#EDE9FE", "align": "left"}
    )
    neo_agent = b.add_box(
        "<b>datum-connect Daemon / Galactic Node</b><br/><font color='#DDD6FE'>• Headless Rust daemon + Go supervisor<br/>• Iroh P2P QUIC + MASQUE CONNECT-IP<br/>• Zero-config dynamic peering via ed25519 identity</font>",
        70, 435, 440, 115,
        {"fillColor": "#4C1D95", "strokeColor": "#A855F7", "fontColor": "#FFFFFF", "strokeWidth": "2", "align": "left"}
    )

    # 2. Hyperscalers Box (Top-Right)
    hyper_bg = b.add_box(
        "<b><font size='3' color='#FED7AA'>HYPERSCALERS &amp; ENTERPRISE CLOUDS</font></b><br/><font color='#FB923C' size='2'>Enterprise Data Lakes • Identity • Relational Databases • Mission-Critical SaaS</font>",
        1390, 130, 480, 440,
        {"fillColor": "#451A03", "strokeColor": "#F59E0B", "strokeWidth": "2", "verticalAlign": "top", "align": "center", "opacity": "90"}
    )
    b.add_box(
        "<b>AWS / GCP / Microsoft Azure / OCI</b><br/><font color='#FDE68A'>• Amazon S3 Training Lakes, RDS, Aurora<br/>• Google BigQuery &amp; Vertex AI Services<br/>• Azure Entra ID / Corporate Active Directory<br/><b>Challenge:</b> Vendor lock-in, proprietary interconnects (DirectConnect/ExpressRoute), egress tax.</font>",
        1410, 200, 440, 100,
        {"fillColor": "#78350F", "strokeColor": "#D97706", "fontColor": "#FEF3C7", "align": "left"}
    )
    b.add_box(
        "<b>Hyperscaler VPCs &amp; Transit Gateways</b><br/><font color='#FDE68A'>• AWS TGW / Private Subnets (172.31.0.0/16)<br/>• GCP Cloud Routers &amp; Interconnect Attachments<br/>• Azure ExpressRoute Gateways</font>",
        1410, 320, 440, 95,
        {"fillColor": "#78350F", "strokeColor": "#D97706", "fontColor": "#FEF3C7", "align": "left"}
    )
    hyper_agent = b.add_box(
        "<b>Interconnect Gateway / Partner Tunnel</b><br/><font color='#FED7AA'>• High-speed BGP Peering (802.1Q VLANs)<br/>• Dynamic IPsec / WireGuard / MASQUE gateway<br/>• Automated BGP route synchronization</font>",
        1410, 435, 440, 115,
        {"fillColor": "#92400E", "strokeColor": "#F59E0B", "fontColor": "#FFFFFF", "strokeWidth": "2", "align": "left"}
    )

    # 3. Last-Mile & Enterprise Edge (Bottom-Left)
    edge_bg = b.add_box(
        "<b><font size='3' color='#A7F3D0'>LAST-MILE PROVIDERS &amp; ENTERPRISE EDGE</font></b><br/><font color='#34D399' size='2'>Private Datacenters • Healthcare &amp; Finance On-Prem • Telco MEC • Dev Endpoints</font>",
        50, 650, 480, 440,
        {"fillColor": "#064E3B", "strokeColor": "#10B981", "strokeWidth": "2", "verticalAlign": "top", "align": "center", "opacity": "90"}
    )
    b.add_box(
        "<b>Enterprise On-Premises &amp; Local Edge</b><br/><font color='#D1FAE5'>• HIPAA/PCI Compliant Private Storage<br/>• Manufacturing IoT / Hospital PACS servers<br/>• Telco 5G User Plane Functions (UPF)<br/>• Developer laptops running datumctl</font>",
        70, 720, 440, 100,
        {"fillColor": "#065F46", "strokeColor": "#059669", "fontColor": "#ECFDF5", "align": "left"}
    )
    b.add_box(
        "<b>Edge Security &amp; Firewall Reality</b><br/><font color='#D1FAE5'>• Strict corporate NAT &amp; stateful firewalls<br/>• No inbound public IP or port forwarding<br/>• Outbound restricted to UDP 443 / HTTPS</font>",
        70, 840, 440, 95,
        {"fillColor": "#065F46", "strokeColor": "#059669", "fontColor": "#ECFDF5", "align": "left"}
    )
    lastmile_agent = b.add_box(
        "<b>datumctl-connect (Rust + Go) Client</b><br/><font color='#A7F3D0'>• Iroh UDP STUN NAT hole punching<br/>• Fallback to global relay network<br/>• Establishes full L3 IP tunnel (CONNECT-IP)</font>",
        70, 955, 440, 115,
        {"fillColor": "#047857", "strokeColor": "#10B981", "fontColor": "#FFFFFF", "strokeWidth": "2", "align": "left"}
    )

    # 4. Public Internet Transit & External Consumers (Bottom-Right)
    inet_bg = b.add_box(
        "<b><font size='3' color='#FECDD3'>PUBLIC INTERNET TRANSIT &amp; EXTERNAL CLIENTS</font></b><br/><font color='#FB7185' size='2'>Tier-1 Transit Providers • Global Anycast Ingress • Mobile &amp; Browser Access</font>",
        1390, 650, 480, 440,
        {"fillColor": "#4C0519", "strokeColor": "#F43F5E", "strokeWidth": "2", "verticalAlign": "top", "align": "center", "opacity": "90"}
    )
    b.add_box(
        "<b>External Users, Mobile &amp; Web Clients</b><br/><font color='#FFE4E6'>• Mobile apps &amp; WebTransport clients<br/>• End consumers hitting inference APIs<br/>• External SaaS API integrations</font>",
        1410, 720, 440, 100,
        {"fillColor": "#881337", "strokeColor": "#E11D48", "fontColor": "#FFF1F2", "align": "left"}
    )
    b.add_box(
        "<b>Tier-1 IP Upstreams &amp; Peering Exchanges</b><br/><font color='#FFE4E6'>• Netactuate, Equinix IX, Telia, Lumen, Cogent<br/>• Low-latency internet routing to regional eyeballing networks</font>",
        1410, 840, 440, 95,
        {"fillColor": "#881337", "strokeColor": "#E11D48", "fontColor": "#FFF1F2", "align": "left"}
    )
    inet_edge = b.add_box(
        "<b>Datum Public Transit Gateway</b><br/><font color='#FECDD3'>• Anycast IPv4/IPv6 BGP edge routing<br/>• Stateful sharded NAT66 masquerade egress<br/>• OWASP Core Rule Set WAF &amp; DDoS shielding</font>",
        1410, 955, 440, 115,
        {"fillColor": "#9F1239", "strokeColor": "#F43F5E", "fontColor": "#FFFFFF", "strokeWidth": "2", "align": "left"}
    )

    # 5. Center: Datum Global Interconnect Platform (vMMR)
    vmmr_bg = b.add_box(
        "<b><font size='4' color='#38BDF8'>DATUM GLOBAL INTERCONNECT: VIRTUAL MEET-ME ROOM (vMMR)</font></b><br/><font color='#94A3B8'>17+ Global Edge PoPs • Ashburn • Silicon Valley • Dallas • Frankfurt • London • Amsterdam • Singapore • Tokyo • Sydney</font>",
        570, 130, 780, 960,
        {"fillColor": "#0B192C", "strokeColor": "#0284C7", "strokeWidth": "3", "verticalAlign": "top", "align": "center", "dashPattern": "5 5"}
    )

    # Center Component A: Dynamic Tunnel Ingress Tier (Iroh + MASQUE)
    tunnel_tier = b.add_box(
        "<b>DYNAMIC TUNNEL TERMINATION TIER (Iroh + MASQUE)</b><br/><font color='#93C5FD' size='2'>Zero-Config Cryptographic Ingress • P2P Hole-Punching • Global Iroh Relays • RFC 9484 CONNECT-IP</font>",
        600, 210, 720, 150,
        {"fillColor": "#1E3A8A", "strokeColor": "#3B82F6", "strokeWidth": "2", "fontColor": "#BFDBFE", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>Iroh P2P Engine</b><br/><font size='1'>• ed25519 node crypto keys<br/>• STUN UDP hole-punching<br/>• 0-RTT direct peer links</font>",
        620, 265, 210, 80,
        {"fillColor": "#172554", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>Global Iroh Relays</b><br/><font size='1'>• MASQUE CONNECT-UDP relay<br/>• Guaranteed NAT fallback<br/>• Per-site /48 IPv6 routable</font>",
        855, 265, 210, 80,
        {"fillColor": "#172554", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>MASQUE Gateways</b><br/><font size='1'>• RFC 9484 CONNECT-IP<br/>• Full L3 IP tunneling<br/>• Dynamic IP &amp; route assign</font>",
        1090, 265, 210, 80,
        {"fillColor": "#172554", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )

    # Center Component B: Private Backbone (Galactic VPC)
    backbone_tier = b.add_box(
        "<b>GALACTIC VPC PRIVATE TRANSIT BACKBONE (SRv6 uSID + VRF)</b><br/><font color='#A5B4FC' size='2'>True Multi-Tenant Kernel Isolation • Segment Routing IPv6 Micro-SIDs • BGP EVPN Overlay</font>",
        600, 390, 720, 230,
        {"fillColor": "#312E81", "strokeColor": "#6366F1", "strokeWidth": "2", "fontColor": "#E0E7FF", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>SRv6 Micro-SID (uSID) Datapath</b><br/><font size='1'>• Encapsulates client packets into IPv6 SRH<br/>• Deterministic policy-based routing<br/>• Zero overlay encapsulation overhead (TC-eBPF)</font>",
        620, 445, 330, 75,
        {"fillColor": "#1E1B4B", "strokeColor": "#818CF8", "fontColor": "#EEF2FF"}
    )
    b.add_box(
        "<b>Linux Kernel VRF Isolation</b><br/><font size='1'>• Cryptographic &amp; routing table partition per tenant<br/>• Overlapping RFC 1918 / 4193 IP support<br/>• Strict tenant-to-tenant isolation</font>",
        970, 445, 330, 75,
        {"fillColor": "#1E1B4B", "strokeColor": "#818CF8", "fontColor": "#EEF2FF"}
    )
    b.add_box(
        "<b>Control Plane: GoBGP + FRR Fabric</b><br/><font size='1'>• Multi-cluster EVPN L3VPN route exchange • Distributed Route Reflectors (RR)<br/>• Fast convergence &amp; sub-second BFD failover across 17+ global PoPs</font>",
        620, 535, 680, 70,
        {"fillColor": "#1E1B4B", "strokeColor": "#818CF8", "fontColor": "#EEF2FF"}
    )

    # Center Component C: Edge Ingress & Egress Engines
    edge_tier = b.add_box(
        "<b>EDGE INGRESS &amp; PUBLIC TRANSIT ENGINES (XDP + Maglev + NAT66)</b><br/><font color='#FDE047' size='2'>High-Performance eBPF Datapath • Line-Rate DSR Load Balancing • Stateful Outbound Transit</font>",
        600, 650, 720, 210,
        {"fillColor": "#422006", "strokeColor": "#EAB308", "strokeWidth": "2", "fontColor": "#FEF08A", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>Stateless Maglev DSR (galactic-gateway)</b><br/><font size='1'>• Line-rate XDP L4 load balancer<br/>• Consistent hashing across backends<br/>• Direct Server Return (DSR) bypasses return bottleneck</font>",
        620, 705, 330, 75,
        {"fillColor": "#713F12", "strokeColor": "#FACC15", "fontColor": "#FEF9C3"}
    )
    b.add_box(
        "<b>Stateful Sharded NAT66 (galactic-nat66)</b><br/><font size='1'>• Masquerades private ULA/VPC IPs to public IPs<br/>• LRU-hashed atomic SNAT connection tracking<br/>• High-throughput outbound internet transit</font>",
        970, 705, 330, 75,
        {"fillColor": "#713F12", "strokeColor": "#FACC15", "fontColor": "#FEF9C3"}
    )
    b.add_box(
        "<b>Envoy Gateway + OWASP ModSecurity WAF + ACME TLS</b><br/><font size='1'>• Layer 7 HTTPProxy &amp; HTTPRoute routing • Automatic Let's Encrypt TLS certificates<br/>• Core Rule Set (CRS) Layer 7 attack filtering &amp; DDoS rate limiting</font>",
        620, 795, 680, 50,
        {"fillColor": "#713F12", "strokeColor": "#FACC15", "fontColor": "#FEF9C3"}
    )

    # Center Component D: Declarative Kubernetes Control Plane
    crd_tier = b.add_box(
        "<b>KUBERNETES-NATIVE DECLARATIVE CONTROL PLANE (NSO &amp; Galactic CRDs)</b><br/><font color='#6EE7B7' size='1'>networking.datumapis.com: Connector • ConnectorClass • ConnectorAdvertisement • ConnectorAttachment<br/>NetworkInterfaceClaim • NetworkGateway • NetworkRule • TrafficProtectionPolicy • BGPRouter</font>",
        600, 880, 720, 95,
        {"fillColor": "#064E3B", "strokeColor": "#10B981", "strokeWidth": "2", "fontColor": "#D1FAE5", "align": "center"}
    )

    # Connectors / Flows between Boxes
    b.add_edge(neo_agent, tunnel_tier, "Dynamic QUIC / MASQUE<br/>(P2P or Relay)", {"strokeColor": "#A855F7", "strokeWidth": "3"})
    b.add_edge(lastmile_agent, tunnel_tier, "Iroh Hole-Punch /<br/>MASQUE CONNECT-IP", {"strokeColor": "#10B981", "strokeWidth": "3"})
    b.add_edge(tunnel_tier, backbone_tier, "VRF Injection /<br/>SRv6 Micro-SID Encapsulation", {"strokeColor": "#38BDF8", "strokeWidth": "3"})
    b.add_edge(backbone_tier, hyper_agent, "Private Transit (SRv6 / BGP)<br/>DirectConnect / Partner VIF", {"strokeColor": "#F59E0B", "strokeWidth": "3"})
    b.add_edge(backbone_tier, edge_tier, "Default Route<br/>(egress_sid)", {"strokeColor": "#EAB308", "strokeWidth": "3"})
    b.add_edge(edge_tier, inet_edge, "BGP Per-Site /48 &amp;<br/>Anycast IPv4/IPv6 Transit", {"strokeColor": "#F43F5E", "strokeWidth": "3"})

    return b

# --- Build Diagram 2: Architecture & Protocol Stack ---
def build_diagram_2():
    b = DrawioDiagramBuilder("2. Architecture & Protocol Stack", 1850, 1100)

    # Header
    b.add_box(
        "<b><font size='5' color='#F8FAFC'>DATUM INTERCONNECT: LAYERED CONTROL &amp; DATA PLANE STACK</font></b><br/><font color='#94A3B8' size='3'>Decoupled Architecture from Declarative Intent down to eBPF/XDP Kernel Datapaths</font>",
        40, 30, 1770, 70,
        {"fillColor": "#1E293B", "strokeColor": "#334155", "fontColor": "#FFFFFF", "align": "center"}
    )

    # Layer 1: Application & Compute Intent
    l1 = b.add_box(
        "<b>LAYER 1: WORKLOADS &amp; USER INTENT</b><br/><font color='#94A3B8' size='2'>Kubernetes Pods, VMs, Neocloud GPU Nodes, Developer Desktops, Enterprise Servers</font>",
        50, 130, 1750, 130,
        {"fillColor": "#1E293B", "strokeColor": "#475569", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box("<b>Neocloud AI Workload</b><br/>Pod / Host with 8x H100 GPUs<br/>Emits training sync &amp; model API calls", 70, 175, 380, 70, {"fillColor": "#2E1065", "strokeColor": "#7C3AED", "fontColor": "#EDE9FE"})
    b.add_box("<b>NetworkInterfaceClaim</b><br/>Compute requests NIC without<br/>knowing internal VPC networking details", 480, 175, 400, 70, {"fillColor": "#0F172A", "strokeColor": "#38BDF8", "fontColor": "#E2E8F0"})
    b.add_box("<b>Hyperscaler Enterprise App</b><br/>AWS RDS PostgreSQL &amp; S3 Lake<br/>Awaiting private replication", 910, 175, 400, 70, {"fillColor": "#451A03", "strokeColor": "#D97706", "fontColor": "#FEF3C7"})
    b.add_box("<b>Last-Mile Client / Edge Device</b><br/>datumctl connect tunnel listen<br/>Local service exposed to global VPC", 1340, 175, 430, 70, {"fillColor": "#064E3B", "strokeColor": "#059669", "fontColor": "#ECFDF5"})

    # Layer 2: Kubernetes Control Plane (NSO + Galactic Operator)
    l2 = b.add_box(
        "<b>LAYER 2: DECLARATIVE CONTROL PLANE (CRDs &amp; OPERATORS)</b><br/><font color='#94A3B8' size='2'>Automated Reconciliation across Management &amp; Data Plane Clusters</font>",
        50, 290, 1750, 160,
        {"fillColor": "#0F172A", "strokeColor": "#0284C7", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box("<b>Connector &amp; ConnectorClass</b><br/>Tracks client device liveness,<br/>ed25519 keys, capabilities (MASQUE, TCP)", 70, 345, 330, 90, {"fillColor": "#0369A1", "strokeColor": "#38BDF8", "fontColor": "#F0F9FF"})
    b.add_box("<b>ConnectorAdvertisement</b><br/>Declares exported L3 subnets<br/>and L4 TCP/UDP target endpoints", 420, 345, 320, 90, {"fillColor": "#0369A1", "strokeColor": "#38BDF8", "fontColor": "#F0F9FF"})
    b.add_box("<b>ConnectorAttachment &amp; VPC</b><br/>Binds connector cryptographic ID<br/>to isolated tenant VRF &amp; allocates IP", 760, 345, 320, 90, {"fillColor": "#0369A1", "strokeColor": "#38BDF8", "fontColor": "#F0F9FF"})
    b.add_box("<b>NetworkGateway &amp; NetworkRule</b><br/>Defines Anycast VIPs, Maglev<br/>backend sets, &amp; DSR routing", 1100, 345, 330, 90, {"fillColor": "#0369A1", "strokeColor": "#38BDF8", "fontColor": "#F0F9FF"})
    b.add_box("<b>TrafficProtectionPolicy</b><br/>OWASP CRS Paranoia Levels,<br/>Rate Limiting, &amp; DDoS shielding", 1450, 345, 320, 90, {"fillColor": "#0369A1", "strokeColor": "#38BDF8", "fontColor": "#F0F9FF"})

    # Layer 3: Dynamic Tunnel Ingress & Relay (Iroh + MASQUE)
    l3 = b.add_box(
        "<b>LAYER 3: DYNAMIC TUNNEL &amp; CONNECTIVITY RUNTIME (Iroh + MASQUE)</b><br/><font color='#94A3B8' size='2'>Overcoming Corporate NATs, Symmetric Firewalls, and Strict Network Boundaries</font>",
        50, 480, 1750, 160,
        {"fillColor": "#172554", "strokeColor": "#2563EB", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box("<b>datum-connect Agent</b><br/>Rust crate + Go supervisor<br/>Runs on hosts, containers, laptops<br/>STUN hole punch + QUIC streams", 70, 535, 390, 90, {"fillColor": "#1E40AF", "strokeColor": "#60A5FA", "fontColor": "#EFF6FF"})
    b.add_box("<b>Iroh Global Relay Mesh</b><br/>Stateless UDP relaying on port 443<br/>Provides 100% traversal fallback<br/>Site-specific routable /48 IPv6", 490, 535, 410, 90, {"fillColor": "#1E40AF", "strokeColor": "#60A5FA", "fontColor": "#EFF6FF"})
    b.add_box("<b>IETF MASQUE Protocol Suite</b><br/>RFC 9484 CONNECT-IP (L3 IP Tunnel)<br/>RFC 9298 CONNECT-UDP (Relaying)<br/>HTTP CONNECT-TCP (Proxying)", 930, 535, 410, 90, {"fillColor": "#1E40AF", "strokeColor": "#60A5FA", "fontColor": "#EFF6FF"})
    b.add_box("<b>Dynamic IP Assignment</b><br/>Allocates client IP inside VPC space<br/>Distributes allowed routes via capsule<br/>HeartbeatAgent liveness renewal", 1370, 535, 400, 90, {"fillColor": "#1E40AF", "strokeColor": "#60A5FA", "fontColor": "#EFF6FF"})

    # Layer 4: Overlay Data Plane (SRv6 + VRF + Maglev DSR)
    l4 = b.add_box(
        "<b>LAYER 4: HIGH-PERFORMANCE OVERLAY DATA PLANE (KERNEL &amp; eBPF)</b><br/><font color='#94A3B8' size='2'>Deterministic Hardware-Grade Routing, Isolation, and Load Balancing in Software</font>",
        50, 670, 1750, 160,
        {"fillColor": "#311042", "strokeColor": "#A855F7", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box("<b>SRv6 Micro-SID (uSID) Engine</b><br/>TC-eBPF decap &amp; encap in kernel<br/>Compresses routing segment lists<br/>Direct Pod-to-Pod cross-cluster paths", 70, 725, 400, 90, {"fillColor": "#581C87", "strokeColor": "#C084FC", "fontColor": "#FAF5FF"})
    b.add_box("<b>Linux Kernel VRF Sandboxing</b><br/>Dedicated routing tables per tenant<br/>Guaranteed cryptographic multi-tenancy<br/>No leaky cross-tenant packet leaks", 500, 725, 400, 90, {"fillColor": "#581C87", "strokeColor": "#C084FC", "fontColor": "#FAF5FF"})
    b.add_box("<b>Stateless Maglev DSR (XDP)</b><br/>Line-rate native eBPF driver hook<br/>Consistent hash-ring load balancing<br/>Direct Server Return: 0 return overhead", 930, 725, 400, 90, {"fillColor": "#581C87", "strokeColor": "#C084FC", "fontColor": "#FAF5FF"})
    b.add_box("<b>Sharded Stateful NAT66 Egress</b><br/>Masquerades private VPC packets to GUA<br/>Atomic linear-probe port reservation<br/>Direct access to public internet APIs", 1360, 725, 410, 90, {"fillColor": "#581C87", "strokeColor": "#C084FC", "fontColor": "#FAF5FF"})

    # Layer 5: Underlay Fabric & Physical Interconnects
    l5 = b.add_box(
        "<b>LAYER 5: GLOBAL UNDERLAY FABRIC &amp; PHYSICAL TRANSIT</b><br/><font color='#94A3B8' size='2'>FRR eBGP Fabric Router • Global Anycast • Tier-1 Transits • 17+ Metros</font>",
        50, 860, 1750, 160,
        {"fillColor": "#1C1917", "strokeColor": "#78716C", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box("<b>fabric-router (FRR eBGP)</b><br/>Underlay BGP peering between physical nodes<br/>Global IPv6 unicast reachability on loopback", 70, 915, 400, 85, {"fillColor": "#292524", "strokeColor": "#A8A29E", "fontColor": "#F5F5F4"})
    b.add_box("<b>BGP EVPN L3VPN Control Plane</b><br/>Embedded GoBGP daemon in galactic-router<br/>Distributes tenant EVPN routes fleet-wide", 500, 915, 400, 85, {"fillColor": "#292524", "strokeColor": "#A8A29E", "fontColor": "#F5F5F4"})
    b.add_box("<b>Per-Site /48 BGP Route Advertisements</b><br/>Site-specific IPv6 allocations to Tier-1s<br/>Enables globally-routable iroh-relay endpoints", 930, 915, 400, 85, {"fillColor": "#292524", "strokeColor": "#A8A29E", "fontColor": "#F5F5F4"})
    b.add_box("<b>Physical Colocation &amp; Cloud Interconnects</b><br/>Equinix Ashburn, Frankfurt, San Jose, etc.<br/>Direct Connect / Cloud Interconnect cross-connects", 1360, 915, 410, 85, {"fillColor": "#292524", "strokeColor": "#A8A29E", "fontColor": "#F5F5F4"})

    return b

# --- Build Diagram 3: Practical Deployment & Packet Flow ---
def build_diagram_3():
    b = DrawioDiagramBuilder("3. Practical Deployment & Packet Flow", 1920, 1150)

    # Header
    b.add_box(
        "<b><font size='5' color='#F8FAFC'>DATUM INTERCONNECT: PRACTICAL DEPLOYMENT &amp; PACKET TRACE</font></b><br/><font color='#94A3B8' size='3'>Real-World Blueprint: CoreWeave GPU Cluster ⟷ Datum Ashburn Edge PoP ⟷ AWS us-east-1 VPC &amp; Internet</font>",
        40, 25, 1840, 70,
        {"fillColor": "#1E293B", "strokeColor": "#334155", "fontColor": "#FFFFFF", "align": "center"}
    )

    # Site 1: Neocloud AI Cluster (Left)
    site1 = b.add_box(
        "<b>SITE A: NEOCLOUD GPU CLUSTER (CoreWeave / Lambda)</b><br/><font color='#C4B5FD'>Host: gpu-worker-node-04 • Subnet: 10.100.1.0/24 • Tenant: tenant-alpha</font>",
        50, 120, 480, 480,
        {"fillColor": "#2E1065", "strokeColor": "#8B5CF6", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>AI Workload Pod (vLLM Serving)</b><br/>IP: 10.100.1.50 • Port: 8000<br/>Needs private access to AWS RDS (172.31.42.10)<br/>Needs public access to HuggingFace models",
        70, 180, 440, 80,
        {"fillColor": "#3B0764", "strokeColor": "#A855F7", "fontColor": "#F3E8FF"}
    )
    b.add_box(
        "<b>Linux Kernel VRF (vrf-tenant-alpha)</b><br/>Table: 1001 • Interface: datum0<br/>Default route via datum0 gateway<br/>Route 172.31.0.0/16 via datum-connect tunnel",
        70, 280, 440, 80,
        {"fillColor": "#3B0764", "strokeColor": "#A855F7", "fontColor": "#F3E8FF"}
    )
    b.add_box(
        "<b>datum-connect Daemon</b><br/>Identity: ed25519:2ovpybgj3snjmch...<br/>Establishes QUIC MASQUE CONNECT-IP tunnel<br/>Connected to Datum Ashburn Edge Gateway",
        70, 380, 440, 80,
        {"fillColor": "#4C1D95", "strokeColor": "#C084FC", "fontColor": "#FFFFFF"}
    )
    site1_out = b.add_box(
        "<b>Host Physical Uplink (eth0)</b><br/>IP: 198.51.100.22 (NAT behind firewall)<br/>Outbound UDP 443 to Datum PoP",
        70, 480, 440, 75,
        {"fillColor": "#4C1D95", "strokeColor": "#C084FC", "fontColor": "#FFFFFF"}
    )

    # Site 2: Datum Edge PoP (Center)
    site2 = b.add_box(
        "<b>DATUM INTERCONNECT EDGE POP (Ashburn us-east-1)</b><br/><font color='#93C5FD'>Node: edge-gw-01.ash • SRv6 Locator: fc00:datum:ashburn::/48 • BGP AS: 65001</font>",
        590, 120, 680, 480,
        {"fillColor": "#0F172A", "strokeColor": "#0284C7", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>Public Dynamic Tunnel Termination (MASQUE Gateway)</b><br/>Public Address: 2607:ed40:1000::10 / 147.75.80.1<br/>Terminates Iroh QUIC &amp; MASQUE CONNECT-IP session<br/>Maps client session to Tenant Alpha VRF",
        610, 180, 640, 75,
        {"fillColor": "#1E3A8A", "strokeColor": "#3B82F6", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>Galactic SRv6 uSID Routing Core &amp; VRF Mesh</b><br/>VRF 1001 (Tenant Alpha)<br/>• Route to 172.31.0.0/16 ➔ Encapsulate to AWS Interconnect Gateway (uSID: fc00:datum:aws::1)<br/>• Default Route (::/0) ➔ Forward to Stateful NAT66 Egress Gateway (egress_sid)",
        610, 275, 640, 85,
        {"fillColor": "#312E81", "strokeColor": "#6366F1", "fontColor": "#EEF2FF"}
    )
    b.add_box(
        "<b>Edge XDP Maglev DSR &amp; NAT66 Tier</b><br/>• Ingress: Anycast VIP 2607:ed40:cafe::100 ➔ Maglev DSR to backend<br/>• Egress: Stateful PAT masquerading to GUA 2607:ed40:1000::masq",
        610, 380, 640, 75,
        {"fillColor": "#713F12", "strokeColor": "#FACC15", "fontColor": "#FEF9C3"}
    )
    site2_out_aws = b.add_box(
        "<b>Private Interconnect Uplink</b><br/>Direct Connect / Partner Cross-Connect to AWS<br/>802.1Q VLAN 400 • BGP Peering",
        610, 480, 310, 75,
        {"fillColor": "#14532D", "strokeColor": "#22C55E", "fontColor": "#DCFCE7"}
    )
    site2_out_inet = b.add_box(
        "<b>Tier-1 IP Transit Uplink</b><br/>Netactuate / Equinix Peering Uplink<br/>eBGP transit /48 advertisement",
        940, 480, 310, 75,
        {"fillColor": "#881337", "strokeColor": "#F43F5E", "fontColor": "#FFE4E6"}
    )

    # Site 3: AWS VPC (Top-Right)
    site3 = b.add_box(
        "<b>SITE B: HYPERSCALER (AWS us-east-1 VPC)</b><br/><font color='#FDE68A'>CIDR: 172.31.0.0/16 • Account: Production</font>",
        1330, 120, 480, 220,
        {"fillColor": "#451A03", "strokeColor": "#F59E0B", "strokeWidth": "2", "verticalAlign": "top"}
    )
    site3_gw = b.add_box(
        "<b>AWS Direct Connect Gateway / VIF</b><br/>BGP ASN: 64512 • Peers with Datum Ashburn PoP<br/>Propagates 10.100.1.0/24 route into AWS VPC Route Table",
        1350, 175, 440, 65,
        {"fillColor": "#78350F", "strokeColor": "#F59E0B", "fontColor": "#FEF3C7"}
    )
    b.add_box(
        "<b>Enterprise PostgreSQL DB (Amazon RDS)</b><br/>Private IP: 172.31.42.10 • Port: 5432<br/>Accepts connection directly from CoreWeave vLLM Pod",
        1350, 255, 440, 65,
        {"fillColor": "#78350F", "strokeColor": "#F59E0B", "fontColor": "#FEF3C7"}
    )

    # Site 4: Public Internet (Bottom-Right)
    site4 = b.add_box(
        "<b>PUBLIC INTERNET DESTINATIONS</b><br/><font color='#FECDD3'>Global Web &amp; Public AI Services</font>",
        1330, 370, 480, 230,
        {"fillColor": "#4C0519", "strokeColor": "#F43F5E", "strokeWidth": "2", "verticalAlign": "top"}
    )
    site4_hf = b.add_box(
        "<b>HuggingFace / Model Hub / GitHub</b><br/>Destination IPv6: 2600:9000:20::1 • Port 443<br/>Sees traffic originating from Datum Masquerade GUA",
        1350, 425, 440, 65,
        {"fillColor": "#881337", "strokeColor": "#FB7185", "fontColor": "#FFF1F2"}
    )
    site4_cli = b.add_box(
        "<b>External Client / Web Browser / Mobile App</b><br/>Sends query to Datum Anycast VIP (2607:ed40:cafe::100)<br/>Replies received directly via DSR from CoreWeave!",
        1350, 505, 440, 75,
        {"fillColor": "#881337", "strokeColor": "#FB7185", "fontColor": "#FFE4E6"}
    )

    # Packet Trace Box (Bottom Half)
    trace_box = b.add_box(
        "<b>STEP-BY-STEP PACKET TRACES ACROSS DATUM INTERCONNECT</b>",
        50, 640, 1760, 460,
        {"fillColor": "#090D16", "strokeColor": "#38BDF8", "strokeWidth": "2", "verticalAlign": "top"}
    )

    # Trace 1: Private Cross-Cloud Transit
    b.add_box(
        "<b>FLOW 1: PRIVATE CROSS-CLOUD TRANSIT (Neocloud GPU ➔ AWS Private RDS)</b><br/>"
        "1. <b>Application Origin:</b> PyTorch Pod on CoreWeave initiates TCP connect to <code>172.31.42.10:5432</code> (AWS RDS).<br/>"
        "2. <b>Kernel VRF Routing:</b> Routing table 1001 directs traffic into <code>datum0</code> dynamic tunnel interface.<br/>"
        "3. <b>MASQUE / QUIC Tunnel:</b> <code>datum-connect</code> wraps IP packet into RFC 9484 CONNECT-IP capsule over QUIC to Datum Ashburn.<br/>"
        "4. <b>SRv6 Micro-SID Encapsulation:</b> Ashburn Gateway translates MASQUE capsule into SRv6 uSID packet: <code>[IPv6: fc00:ash:: ➔ fc00:aws:: | Inner IP: 10.100.1.50 ➔ 172.31.42.10]</code>.<br/>"
        "5. <b>Backbone Transit &amp; Decapsulation:</b> Packet crosses Datum private optical transit; decapsulated at AWS Direct Connect Gateway.<br/>"
        "6. <b>Arrival:</b> RDS Postgres receives clean, private packet from <code>10.100.1.50</code> with zero public IP exposure or NAT rewriting!",
        70, 690, 840, 180,
        {"fillColor": "#1E293B", "strokeColor": "#3B82F6", "fontColor": "#E2E8F0", "align": "left"}
    )

    # Trace 2: Public Internet Egress
    b.add_box(
        "<b>FLOW 2: PUBLIC INTERNET EGRESS WITH STATEFUL NAT66 (Neocloud GPU ➔ Internet API)</b><br/>"
        "1. <b>Application Origin:</b> GPU worker requests model weights from HuggingFace (<code>2600:9000:20::1:443</code>).<br/>"
        "2. <b>Default Route Match:</b> VRF default route forwards packet across dynamic tunnel to Datum Edge Gateway with <code>egress_sid</code>.<br/>"
        "3. <b>Stateful NAT66 Masquerade:</b> <code>galactic-nat66</code> allocates port in LRU connection table; translates private source to <code>2607:ed40:1000::masq:42188</code>.<br/>"
        "4. <b>Internet Transit:</b> Gateway forwards packet to Netactuate Tier-1 upstream.<br/>"
        "5. <b>Return Path:</b> HuggingFace replies to <code>2607:ed40:1000::masq:42188</code>. Edge gateway looks up LRU table, DNATs back to pod address, pushes SRv6 return header, and forwards across dynamic tunnel back to CoreWeave!",
        940, 690, 850, 180,
        {"fillColor": "#1E293B", "strokeColor": "#EAB308", "fontColor": "#E2E8F0", "align": "left"}
    )

    # Trace 3: Public Ingress with Maglev DSR
    b.add_box(
        "<b>FLOW 3: HIGH-PERFORMANCE INGRESS VIA STATELESS MAGLEV DSR (External User ➔ Neocloud API)</b><br/>"
        "1. <b>Client Ingress:</b> External client sends HTTP request to Anycast VIP <code>2607:ed40:cafe::100:443</code>.<br/>"
        "2. <b>Stateless Consistent Hashing:</b> <code>galactic-gateway</code> native XDP hook hashes 5-tuple into Maglev lookup table, picking CoreWeave backend <code>10.100.1.50</code>.<br/>"
        "3. <b>SRv6 Encap (No NAT):</b> Gateway pushes outer SRv6 header addressed to worker's uSID. <b>Packet payload and original client IP are NOT rewritten</b>.<br/>"
        "4. <b>Direct Server Return (DSR):</b> Worker receives packet, processes request, and <b>transmits response DIRECTLY to client IP</b> via Datum egress transit, completely bypassing the gateway on the return path! Eliminates gateway return bandwidth saturation.",
        70, 890, 1720, 170,
        {"fillColor": "#1E293B", "strokeColor": "#10B981", "fontColor": "#E2E8F0", "align": "left"}
    )

    # Edges
    b.add_edge(site1_out, site2, "Dynamic QUIC / MASQUE<br/>(Private + Public Transit)", {"strokeColor": "#A855F7", "strokeWidth": "3"})
    b.add_edge(site2_out_aws, site3_gw, "Direct Connect / 802.1Q<br/>Private VPC Routes", {"strokeColor": "#F59E0B", "strokeWidth": "3"})
    b.add_edge(site2_out_inet, site4_hf, "Tier-1 IP Transit<br/>BGP Per-Site /48", {"strokeColor": "#F43F5E", "strokeWidth": "3"})

    return b

# --- Build Diagram 4: Dynamic Tunnel & Agent Lifecycle ---
def build_diagram_4():
    b = DrawioDiagramBuilder("4. Dynamic Tunnel & Agent Lifecycle", 1850, 1100)

    # Header
    b.add_box(
        "<b><font size='5' color='#F8FAFC'>DATUM CONNECT: DYNAMIC TUNNEL ARCHITECTURE &amp; AGENT LIFECYCLE</font></b><br/><font color='#94A3B8' size='3'>How Iroh P2P NAT Traversal, Cryptographic Identity, and MASQUE CONNECT-IP Operate in Practice</font>",
        40, 30, 1770, 70,
        {"fillColor": "#1E293B", "strokeColor": "#334155", "fontColor": "#FFFFFF", "align": "center"}
    )

    # Phase 1: Identity & Supervisor Startup
    p1 = b.add_box(
        "<b>PHASE 1: INITIALIZATION &amp; SUPERVISOR</b><br/><font color='#93C5FD'>Two-Binary Architecture • State Isolation</font>",
        50, 130, 390, 850,
        {"fillColor": "#0F172A", "strokeColor": "#3B82F6", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>1. datumctl Invocation</b><br/>User or systemd executes:<br/><code>datumctl connect tunnel run ...</code><br/>Go supervisor initializes.",
        70, 190, 350, 80,
        {"fillColor": "#1E293B", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>2. Subprocess Management</b><br/>Go supervisor spawns headless<br/>Rust binary <code>datum-connect</code>.<br/>• Stderr ➔ Human status lines<br/>• Stdout ➔ JSON lifecycle events",
        70, 290, 350, 100,
        {"fillColor": "#1E293B", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>3. Cryptographic Identity</b><br/>Generates/loads persistent Ed25519<br/>keypair in <code>~/.local/share/datumctl/</code>.<br/>Public key (NodeId) serves as global cryptographic identity.",
        70, 410, 350, 100,
        {"fillColor": "#1E293B", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>4. Credential Resolution</b><br/>Executes credential helper via<br/><code>DATUM_CREDENTIALS_HELPER</code>.<br/>Acquires scoped OAuth token for<br/>Datum Cloud API authentication.",
        70, 530, 350, 95,
        {"fillColor": "#1E293B", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>5. Project Control Plane Bind</b><br/>Connects to Kubernetes API server.<br/>Reconciles <code>Connector</code> custom resource with <code>PublicKey</code> connection details.",
        70, 645, 350, 95,
        {"fillColor": "#1E293B", "strokeColor": "#60A5FA", "fontColor": "#DBEAFE"}
    )
    b.add_box(
        "<b>Key Benefit: Crash Isolation</b><br/>Supervisor restarts Rust binary on panic; isolates user credentials from child memory.",
        70, 760, 350, 85,
        {"fillColor": "#0F2942", "strokeColor": "#38BDF8", "fontColor": "#E0F2FE"}
    )

    # Phase 2: NAT Traversal & Hole Punching
    p2 = b.add_box(
        "<b>PHASE 2: NAT TRAVERSAL &amp; HOLE PUNCHING</b><br/><font color='#A7F3D0'>Iroh P2P Engine • STUN / DERP • Zero Inbound Ports</font>",
        470, 130, 410, 850,
        {"fillColor": "#064E3B", "strokeColor": "#10B981", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>1. Discover Local &amp; WAN Endpoints</b><br/>Agent probes local interfaces and contacts Home Relay via STUN.<br/>Learns public IP, mapped port, and NAT type (Cone vs Symmetric).",
        490, 190, 370, 95,
        {"fillColor": "#065F46", "strokeColor": "#34D399", "fontColor": "#ECFDF5"}
    )
    b.add_box(
        "<b>2. Home Relay Registration</b><br/>Publishes reachable DERP endpoint to<br/>Datum Home Relay (e.g. <code>relay.ash.datum.net</code>).<br/>Relay publishes /48 BGP prefix.",
        490, 305, 370, 95,
        {"fillColor": "#065F46", "strokeColor": "#34D399", "fontColor": "#ECFDF5"}
    )
    b.add_box(
        "<b>3. Simultaneous UDP Hole Punch</b><br/>Both endpoints exchange candidates out-of-band via relay.<br/>Simultaneously send UDP packets to punch holes in stateful firewalls.",
        490, 420, 370, 95,
        {"fillColor": "#065F46", "strokeColor": "#34D399", "fontColor": "#ECFDF5"}
    )
    b.add_box(
        "<b>4. Path Decision Matrix</b><br/>• <b>Direct P2P:</b> If hole-punch succeeds, upgrade immediately to 0-RTT direct QUIC.<br/>• <b>Relay Fallback:</b> If symmetric enterprise NAT blocks UDP, tunnel smoothly through Datum Relay over port 443.",
        490, 535, 370, 120,
        {"fillColor": "#065F46", "strokeColor": "#34D399", "fontColor": "#ECFDF5"}
    )
    b.add_box(
        "<b>5. Encrypted QUIC Handshake</b><br/>TLS 1.3 handshake authenticated by<br/>Ed25519 node keys. Perfect forward secrecy, immune to IP spoofing.",
        490, 675, 370, 90,
        {"fillColor": "#065F46", "strokeColor": "#34D399", "fontColor": "#ECFDF5"}
    )
    b.add_box(
        "<b>Zero Firewall Changes Needed</b><br/>Works through hotel Wi-Fi, strict enterprise NAT, and cellular without open ports.",
        490, 785, 370, 80,
        {"fillColor": "#022C22", "strokeColor": "#10B981", "fontColor": "#D1FAE5"}
    )

    # Phase 3: MASQUE CONNECT-IP Tunnel
    p3 = b.add_box(
        "<b>PHASE 3: MASQUE PROTOCOL NEGOTIATION</b><br/><font color='#FED7AA'>RFC 9484 CONNECT-IP • L3 Encapsulation</font>",
        910, 130, 410, 850,
        {"fillColor": "#451A03", "strokeColor": "#F59E0B", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>1. HTTP/3 CONNECT-IP Request</b><br/>Agent opens bidirectional QUIC stream and issues standard HTTP/3 extended CONNECT request for <code>masque://datum-gateway</code>.",
        930, 190, 370, 95,
        {"fillColor": "#78350F", "strokeColor": "#FBBF24", "fontColor": "#FEF3C7"}
    )
    b.add_box(
        "<b>2. Capability Negotiation</b><br/>Gateway checks <code>Connector.spec.capabilities</code>:<br/>• MASQUE (RFC 9484)<br/>• CONNECT-IP (L3 IP packets)<br/>• CONNECT-TCP (HTTP proxying)",
        930, 305, 370, 95,
        {"fillColor": "#78350F", "strokeColor": "#FBBF24", "fontColor": "#FEF3C7"}
    )
    b.add_box(
        "<b>3. Address &amp; Route Assignment</b><br/>Gateway responds with 200 OK + Capsule Frames:<br/>• <code>ADDRESS_ASSIGN</code>: 10.100.1.50/24<br/>• <code>ROUTE_ADVERTISEMENT</code>: 172.31.0.0/16, ::/0",
        930, 420, 370, 100,
        {"fillColor": "#78350F", "strokeColor": "#FBBF24", "fontColor": "#FEF3C7"}
    )
    b.add_box(
        "<b>4. Kernel Device Provisioning</b><br/>Agent creates virtual TUN interface (<code>datum0</code>); binds to kernel VRF.<br/>Routes for target VPC subnets programmed into local routing table.",
        930, 540, 370, 95,
        {"fillColor": "#78350F", "strokeColor": "#FBBF24", "fontColor": "#FEF3C7"}
    )
    b.add_box(
        "<b>5. Capsule Frame Forwarding</b><br/>Raw IP packets routed to <code>datum0</code> are encapsulated inside MASQUE IP capsules over QUIC datagrams.",
        930, 655, 370, 90,
        {"fillColor": "#78350F", "strokeColor": "#FBBF24", "fontColor": "#FEF3C7"}
    )
    b.add_box(
        "<b>IETF Standard Compliant</b><br/>Standard RFC 9484 wire format. Allows future browser WebTransport clients without proprietary clients.",
        930, 765, 370, 85,
        {"fillColor": "#291500", "strokeColor": "#F59E0B", "fontColor": "#FEF3C7"}
    )

    # Phase 4: Liveness, Heartbeat & Self-Healing
    p4 = b.add_box(
        "<b>PHASE 4: LIVENESS &amp; SELF-HEALING</b><br/><font color='#DDD6FE'>Kube Lease Renewal • Seamless Migration</font>",
        1350, 130, 450, 850,
        {"fillColor": "#2E1065", "strokeColor": "#8B5CF6", "strokeWidth": "2", "verticalAlign": "top"}
    )
    b.add_box(
        "<b>1. HeartbeatAgent &amp; LeaseRef</b><br/>Rust agent runs async heartbeat task. Periodically updates <code>coordination.k8s.io/v1 Lease</code> referenced in <code>Connector.status.leaseRef</code>.<br/>Guarantees operator knows agent is healthy.",
        1370, 190, 410, 100,
        {"fillColor": "#3B0764", "strokeColor": "#A855F7", "fontColor": "#F3E8FF"}
    )
    b.add_box(
        "<b>2. Failure Detection &amp; Drop Prevention</b><br/>If agent process dies or loses network, Lease expires after 30s.<br/>Controller sets <code>Connector.status.Ready = False</code>.<br/>Galactic routes smoothly re-converge to standby gateways.",
        1370, 310, 410, 105,
        {"fillColor": "#3B0764", "strokeColor": "#A855F7", "fontColor": "#F3E8FF"}
    )
    b.add_box(
        "<b>3. QUIC Connection Migration</b><br/>If physical IP changes (e.g. Wi-Fi ➔ Cellular, or laptop sleep/wake), QUIC connection ID persists!<br/><b>Active TCP connections over MASQUE tunnel DO NOT DROP.</b>",
        1370, 435, 410, 105,
        {"fillColor": "#3B0764", "strokeColor": "#A855F7", "fontColor": "#F3E8FF"}
    )
    b.add_box(
        "<b>4. Auto-Reconnection &amp; Retry</b><br/>If link drops entirely, agent executes exponential backoff.<br/>Re-probes STUN and relays.<br/>Transparently resumes session within milliseconds.",
        1370, 560, 410, 95,
        {"fillColor": "#3B0764", "strokeColor": "#A855F7", "fontColor": "#F3E8FF"}
    )
    b.add_box(
        "<b>5. Clean Teardown &amp; GC</b><br/>On SIGTERM/Ctrl+C, supervisor notifies Rust child.<br/>Removes TUN interface, clears routes, and cleans up CRD status cleanly.",
        1370, 675, 410, 90,
        {"fillColor": "#3B0764", "strokeColor": "#A855F7", "fontColor": "#F3E8FF"}
    )
    b.add_box(
        "<b>Zero-Downtime Resilience</b><br/>Hardened against packet loss, route flaps, and dynamic interface switches.",
        1370, 785, 410, 80,
        {"fillColor": "#19053B", "strokeColor": "#C084FC", "fontColor": "#EDE9FE"}
    )

    # Cross-phase flow arrows
    b.add_edge(p1, p2, "Child Spawned &amp; Identity Ready", {"strokeColor": "#38BDF8", "strokeWidth": "2"})
    b.add_edge(p2, p3, "P2P or Relay Path Established", {"strokeColor": "#10B981", "strokeWidth": "2"})
    b.add_edge(p3, p4, "L3 Tunnel Active &amp; Interfaces Up", {"strokeColor": "#F59E0B", "strokeWidth": "2"})

    return b

def main():
    os.makedirs("/home/darragh/dev/proj/datum/interconnect/diagrams", exist_ok=True)
    
    # 1. Build all 4 diagram objects
    d1 = build_diagram_1()
    d2 = build_diagram_2()
    d3 = build_diagram_3()
    d4 = build_diagram_4()

    # 2. Build multi-page .drawio XML
    root = ET.Element("mxfile", {
        "host": "app.diagrams.net",
        "modified": "2026-09-03T20:30:00.000Z",
        "agent": "Datum Architecture Engine",
        "version": "24.0.0",
        "type": "device"
    })

    root.append(d1.to_xml("diagram-1"))
    root.append(d2.to_xml("diagram-2"))
    root.append(d3.to_xml("diagram-3"))
    root.append(d4.to_xml("diagram-4"))

    multi_page_path = "/home/darragh/dev/proj/datum/interconnect/datum-interconnect-architecture.drawio"
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(multi_page_path, encoding="utf-8", xml_declaration=True)
    print(f"Generated multi-page Draw.io file at: {multi_page_path}")

    # 3. Also export individual .drawio files for convenience
    individual_diagrams = [
        ("1-ecosystem-virtual-meet-me-room.drawio", d1),
        ("2-control-and-data-plane-stack.drawio", d2),
        ("3-practical-deployment-and-packet-flow.drawio", d3),
        ("4-dynamic-tunnel-and-agent-lifecycle.drawio", d4),
    ]

    for fname, diag in individual_diagrams:
        indiv_root = ET.Element("mxfile", {
            "host": "app.diagrams.net",
            "modified": "2026-09-03T20:30:00.000Z",
            "agent": "Datum Architecture Engine",
            "version": "24.0.0",
            "type": "device"
        })
        indiv_root.append(diag.to_xml("diagram-page"))
        out_path = os.path.join("/home/darragh/dev/proj/datum/interconnect/diagrams", fname)
        indiv_tree = ET.ElementTree(indiv_root)
        ET.indent(indiv_tree, space="  ", level=0)
        indiv_tree.write(out_path, encoding="utf-8", xml_declaration=True)
        print(f"Generated individual diagram at: {out_path}")

    print("All Draw.io diagrams successfully generated and verified!")

if __name__ == "__main__":
    main()
