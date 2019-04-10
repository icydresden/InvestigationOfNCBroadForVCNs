//
// Created by lab on 26.04.18.
//

//#include "ns3/core-module.h"
//#include "ns3/network-module.h"
//#include "ns3/internet-module.h"
//#include "ns3/point-to-point-module.h"
//#include "ns3/applications-module.h"
//#include "ns3/csma-module.h"
//#include "ns3/internet-module.h"
//#include "ns3/wifi-module.h"
//
//#include "ns3/netanim-module.h"
//#include "ns3/mobility-module.h"

//           nB
//           ^
//           |
//           |
//n0 -----------------> n1
//           |
//           |
//           nA



#include "ns3/core-module.h"
#inlcude "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/wifi-module.h"
#include "ns3/netanim-module.h"
#include "ns3/mobility-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("First Test NS3 File");
int
main(int argc, char *argv[])
{
    uint32_t nWifi = 4;
    bool verbose = true;

    CommandLine cmd;
    cmd.AddValue ("nWifi", "Number of wifi STA devices", nWifi);
    cmd.Parse(argc, argv);

//    Time::SetResolution (Time::NS);

    if(verbose)
    {
        LogComponentEnable ("nWifi Components", LOG_LEVEL_INFO);
    }

    NodeContainer wifiNodes;
    wifiNodes.Create(nWifi);

    YansWifiChannelHelper channel = YansWifiChannelHelper::Default();
    YansWifiPhyHelper phy = YansWifiPhyHelper::Default();
    phy.SetChannel (channel.Create());

    WifiHelper wifi;
    wifi.SetRemoteStationManager ("ns3::AarfWifiManager");

    WifiMacHelper mac;
    Ssid ssid = Ssid ("ns-3-ssid");

//
//    YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
//    YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
//    phy.SetChannel (channel.Create ());
//
//    WifiHelper wifi;
//    wifi.SetRemoteStationManager ("ns3::AarfWifiManager");
//
//    WifiMacHelper mac;
//    Ssid ssid = Ssid ("ns-3-ssid");
//    mac.SetType ("ns3::StaWifiMac",
//                 "Ssid", SsidValue (ssid),
//                 "ActiveProbing", BooleanValue (false));
//
//    NetDeviceContainer staDevices;
//    staDevices = wifi.Install (phy, mac, wifiStaNodes);
//
//    mac.SetType ("ns3::ApWifiMac",
//                 "Ssid", SsidValue (ssid));
//
//    NetDeviceContainer apDevices;
//    apDevices = wifi.Install (phy, mac, wifiApNode);
//
//    MobilityHelper mobility;
//
//    mobility.SetPositionAllocator ("ns3::GridPositionAllocator",
//                                   "MinX", DoubleValue (0.0),
//                                   "MinY", DoubleValue (0.0),
//                                   "DeltaX", DoubleValue (5.0),
//                                   "DeltaY", DoubleValue (10.0),
//                                   "GridWidth", UintegerValue (3),
//                                   "LayoutType", StringValue ("RowFirst"));
//
//    mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
//                               "Bounds", RectangleValue (Rectangle (0, 75, 0, 75)));
//    mobility.Install (wifiStaNodes);
//
//    mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
//    mobility.Install (wifiApNode);
//    mobility.Install (csmaNodes);
//
//    InternetStackHelper stack;
//    stack.Install (csmaNodes);
//    stack.Install (wifiApNode);
//    stack.Install (wifiStaNodes);

}