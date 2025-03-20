package com.brunoxabreu.lead_enrichment.integration;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import java.util.Map;

@FeignClient(name = "clearbit", url = "${services.clearbit.base-url}")
public interface ClearbitClient {
    @GetMapping("/people/find")
    Map<String, Object> buscarPessoa(
            @RequestHeader("Authorization") String apiKey,
            @RequestParam("email") String email
    );
} 