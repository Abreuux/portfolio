package com.brunoxabreu.lead_enrichment.integration;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.Map;

@FeignClient(name = "hunter", url = "${services.hunter.base-url}")
public interface HunterClient {
    @GetMapping("/email-finder")
    Map<String, Object> buscarEmail(
            @RequestHeader("Authorization") String apiKey,
            @RequestParam("full_name") String nome,
            @RequestParam("company") String empresa
    );
} 