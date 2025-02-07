/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2014 Steinwurf ApS
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

// This class implements RLNC (random linear network coding) in
// the application layer for a broadcast topology.

#pragma once

#include <kodocpp/kodocpp.hpp>
#include <fstream> // !1

class Broadcast
{
public:

  Broadcast (const kodocpp::codec codeType,
             const kodocpp::field field,
             const uint32_t users,
             const uint32_t generationSize,
             const uint32_t packetSize,
             const ns3::Ptr<ns3::Socket>& source,
             const std::vector<ns3::Ptr<ns3::Socket>>& sinks)
    : m_codeType (codeType),
      m_field (field),
      m_users (users),
      m_generationSize (generationSize),
      m_packetSize (packetSize),
      m_source (source),
      m_sinks (sinks)
  {
    srand(static_cast<uint32_t>(time(0)));

    // Create factories using the supplied parameters
    kodocpp::encoder_factory encoderFactory (m_codeType, m_field,
      m_generationSize, m_packetSize);
    kodocpp::decoder_factory decoderFactory (m_codeType, m_field,
      m_generationSize, m_packetSize);

    // Create encoder and disable systematic mode
    m_encoder = encoderFactory.build ();
    m_encoder.set_systematic_off ();

    // Initialize the encoder data buffer
    m_encoderBuffer.resize (m_encoder.block_size ());
    m_encoder.set_const_symbols (m_encoderBuffer.data (),
      m_encoder.block_size ());
    m_payload.resize (m_encoder.payload_size ());

    // Create decoders
    m_decoderBuffers.resize (m_users);
    for (uint32_t n = 0; n < m_users; n++)
      {
        kodocpp::decoder decoder = decoderFactory.build ();

        // Add custom trace callback to each decoder
        auto callback = [](const std::string& zone, const std::string& data)
          {
            std::set<std::string> filters =
              { "decoder_state", "symbol_coefficients_before_read_symbol" };
            if (filters.count (zone))
              {
                std::cout << zone << ":" << std::endl;
                std::cout << data << std::endl;
              }
          };
        decoder.set_trace_callback (callback);

        // Create data buffer for the decoder
        m_decoderBuffers[n].resize (decoder.block_size ());
        decoder.set_mutable_symbols (m_decoderBuffers[n].data (),
          decoder.block_size ());

        m_decoders.emplace_back (decoder);
      }

    // Initialize transmission count
    m_transmissionCount = 0;
  }

  void SendPacket (ns3::Ptr<ns3::Socket> socket, ns3::Time pktInterval)
  {
    bool allDecoded = true;

    for (uint32_t n = 0; n < m_users; n++)
      {
        allDecoded = allDecoded && m_decoders[n].is_complete ();
      }

    if (!allDecoded)
      {
        std::cout << "+----------------------+" << std::endl;
        std::cout << "|Sending a coded packet|" << std::endl;
        std::cout << "+----------------------+" << std::endl;
        uint32_t bytesUsed = m_encoder.write_payload (&m_payload[0]);
        auto packet = ns3::Create<ns3::Packet> (&m_payload[0], bytesUsed);
        socket->Send (packet);
        m_transmissionCount++;

        ns3::Simulator::Schedule (pktInterval, &Broadcast::SendPacket, this,
          socket, pktInterval);
      }
    else
      {
        std::cout << "Decoding completed! Total transmissions: "
          << m_transmissionCount << std::endl;
//        std::ofstream ofs("kodoWIFIout.txt");
//        ofs<<m_packetSize <<" "<<m_transmissionCount<<std::endl;
//        ofs.close();
        socket->Close ();
      }
  }

  void ReceivePacket (ns3::Ptr<ns3::Socket> socket)
  {
    // Find the decoder index based on the socket
    auto it = std::find(m_sinks.begin (), m_sinks.end (), socket);
    auto n = std::distance (m_sinks.begin (), it);

    std::cout << "Received a packet at Decoder " << n + 1 << std::endl;

    std::vector<uint8_t> payload (m_decoders[n].payload_size ());

    // Pass the packet payload to the appropriate decoder
    auto packet = socket->Recv ();
    packet->CopyData (&payload[0], m_decoders[n].payload_size ());
    m_decoders[n].read_payload (&payload[0]);
  }

private:

  const kodocpp::codec m_codeType;
  const kodocpp::field m_field;
  const uint32_t m_users;
  const uint32_t m_generationSize;
  const uint32_t m_packetSize;

  ns3::Ptr<ns3::Socket> m_source;
  std::vector<ns3::Ptr<ns3::Socket>> m_sinks;
  kodocpp::encoder m_encoder;
  std::vector<uint8_t> m_encoderBuffer;
  std::vector<kodocpp::decoder> m_decoders;
  std::vector<std::vector<uint8_t>> m_decoderBuffers;

  std::vector<uint8_t> m_payload;
  uint32_t m_transmissionCount;
};
