package com.brunoxabreu.commercial_bpms.controller;

import com.brunoxabreu.commercial_bpms.domain.model.PropostaComercial;
import com.brunoxabreu.commercial_bpms.service.PropostaComercialService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/propostas")
@RequiredArgsConstructor
public class PropostaComercialController {

    private final PropostaComercialService propostaService;

    @PostMapping
    public ResponseEntity<PropostaComercial> criarProposta(@RequestBody PropostaComercial proposta) {
        return ResponseEntity.ok(propostaService.iniciarProcesso(proposta));
    }

    @PostMapping("/{id}/aprovar")
    public ResponseEntity<PropostaComercial> aprovarProposta(@PathVariable Long id) {
        return ResponseEntity.ok(propostaService.aprovarProposta(id));
    }

    @PostMapping("/{id}/rejeitar")
    public ResponseEntity<PropostaComercial> rejeitarProposta(
            @PathVariable Long id,
            @RequestParam String observacoes) {
        return ResponseEntity.ok(propostaService.rejeitarProposta(id, observacoes));
    }
} 