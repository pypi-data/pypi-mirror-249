from peft import LoraConfig, get_peft_model, PeftModel

from ..core import Algorithm
from ..path import local_copy, in_memory_storage
from transformers import Trainer, LlamaForCausalLM
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoConfig
import transformers


class FineTuneLLM(Algorithm):

    def __init__(self, hparams, **kwargs):

        networks = None
        config = None
        if hparams.get('reload_path', None) is None:
            config = self.load_configuration(hparams)
            model = self.load_lora_model(hparams, config=config)
            networks = {'llm': model}

        self.tokenizer = self.load_tokenizer(hparams, config=config)
        super().__init__(hparams, networks=networks, **kwargs)

    @staticmethod
    def load_configuration(hparams):
        return AutoConfig.from_pretrained(hparams.model, cache_dir=hparams.hf_cache_dir)

    @staticmethod
    def load_tokenizer(hparams, config=None):
        if config is None:
            config = FineTuneLLM.load_configuration(hparams)
        return AutoTokenizer.from_pretrained(hparams.model, config=config)

    @staticmethod
    def load_model(hparams, config=None):

        if config is None:
            config = FineTuneLLM.load_configuration(hparams)

        model = AutoModelForCausalLM.from_pretrained(hparams.model, config=config, load_in_8bit=hparams.load_in_8bit)
        return model

    @staticmethod
    def load_lora_model(hparams, config=None, model=None):

        if model is None:
            model = FineTuneLLM.load_model(hparams, config=config)

        lora_config = LoraConfig(r=hparams.lora_r, lora_alpha=hparams.lora_alpha,
                                 target_modules=hparams.target_modules, lora_dropout=hparams.lora_dropout,
                                 bias=hparams.lora_bias, fan_in_fan_out=hparams.lora_fan_in_fan_out,
                                 modules_to_save=hparams.modules_to_save,
                                 layers_to_transform=hparams.layers_to_transform,
                                 task_type="CAUSAL_LM")

        model = get_peft_model(model, lora_config)
        return model

    def train_iteration(self, sample=None, label=None, index=None, counter=None, subset=None, training=True, **kwargs):
        net = self.networks['llm']

        res = net(input_ids=sample['input_ids'], attention_mask=sample['attention_mask'], labels=sample['input_ids'])
        self.apply(res.loss)

    def save_checkpoint(self, path=None, networks=True, optimizers=True, schedulers=True,
                        processors=True, scaler=True, scalers=True, swa_schedulers=True, swa_networks=True,
                        hparams=True, aux=None, pickle_model=False):

        in_memory_path = in_memory_storage(mode='file')
        with local_copy(in_memory_path, as_beam_path=False) as local_path:
            self.networks['llm'].save_pretrained(local_path)

        if networks:
            if aux is None:
                aux = {}
            aux['lora'] = in_memory_path.data

        return super().save_checkpoint(path=path, networks=False, optimizers=optimizers, schedulers=schedulers,
                        processors=processors, scaler=scaler, scalers=scalers, swa_schedulers=swa_schedulers, swa_networks=swa_networks,
                        hparams=hparams, aux=aux, pickle_model=pickle_model)

    def load_checkpoint(self, path_or_state, strict=True, networks=True, optimizers=True, schedulers=True,
                        processors=True, scaler=True, scalers=True, swa_schedulers=True, swa_networks=True,
                        hparams=True, load_epoch=True):

        aux = super().load_checkpoint(path_or_state, networks=False, optimizers=optimizers, schedulers=schedulers,
                        processors=processors, scaler=scaler, scalers=scalers, swa_schedulers=swa_schedulers, swa_networks=swa_networks,
                        hparams=hparams)

        in_memory_path = in_memory_storage(mode='file', data=aux.pop('lora'))
        with local_copy(in_memory_path, as_beam_path=False) as local_path:
            model = self.load_model(self.hparams)
            model = PeftModel.from_pretrained(model, local_path, is_trainable=True)
            self.add_network(model, 'llm')
            # self.networks['llm'].from_pretrained(local_path)

        return aux