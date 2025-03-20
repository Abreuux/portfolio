package com.brunoxabreu.lead_enrichment.integration;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.Map;

@FeignClient(name = "linkedin", url = "${services.linkedin.base-url}")
public interface LinkedInClient {
    @GetMapping("/people")
    Map<String, Object> buscarPessoa(
            @RequestHeader("Authorization") String apiKey,
            @RequestParam("q") String query
    );
} 