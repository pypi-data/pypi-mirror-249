<template>
  <mobile-fullscreen-dialog v-model="dialog" max-width="500px">
    <template #activator="{ on, attrs }">
      <slot name="activator" v-bind="{ on, attrs }" />
    </template>

    <template #title>
      <slot name="title">
        <span class="text-h5">{{
          isCreate ? $t(createItemI18nKey) : $t(editItemI18nKey)
        }}</span>
      </slot>
    </template>

    <template #content>
      <v-form v-model="valid">
        <v-container>
          <v-row>
            <v-col
              cols="12"
              :sm="field.cols || 6"
              v-for="field in fields"
              :key="field.value"
            >
              <slot
                :label="field.text"
                :name="field.value + '.field'"
                :attrs="buildAttrs(itemModel, field)"
                :on="buildOn(dynamicSetter(itemModel, field.value))"
                :is-create="isCreate"
                :item="itemModel"
                :setter="buildExternalSetter(itemModel)"
              >
                <v-text-field
                  :label="field.text"
                  filled
                  v-model="itemModel[field.value]"
                ></v-text-field>
              </slot>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </template>

    <template #actions>
      <cancel-button @click="$emit('cancel')" />
      <save-button @click="save" :loading="loading" :disabled="!valid" />
    </template>
  </mobile-fullscreen-dialog>
</template>

<script>
import SaveButton from "../buttons/SaveButton.vue";
import CancelButton from "../buttons/CancelButton.vue";
import MobileFullscreenDialog from "./MobileFullscreenDialog.vue";

export default {
  name: "DialogObjectForm",
  components: {
    CancelButton,
    SaveButton,
    MobileFullscreenDialog,
  },
  data() {
    return {
      loading: false,
      valid: false,
      firstInitDone: false,
      itemModel: {},
    };
  },
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    createItemI18nKey: {
      type: String,
      required: false,
      default: "actions.create",
    },
    createSuccessMessageI18nKey: {
      type: String,
      required: false,
      default: "status.object_create_success",
    },
    editItemI18nKey: {
      type: String,
      required: false,
      default: "actions.edit",
    },
    editSuccessMessageI18nKey: {
      type: String,
      required: false,
      default: "status.object_edit_success",
    },
    gqlCreateMutation: {
      type: Object,
      required: false,
      default: undefined,
    },
    gqlPatchMutation: {
      type: Object,
      required: false,
      default: undefined,
    },
    fields: {
      type: Array,
      required: true,
    },
    itemTitleAttribute: {
      type: String,
      required: false,
      default: "name",
    },
    defaultItem: {
      type: Object,
      required: true,
    },
    editItem: {
      type: Object,
      required: false,
      default: undefined,
    },
    forceModelItemUpdate: {
      type: Boolean,
      required: false,
      default: false,
    },
    getCreateData: {
      type: Function,
      required: false,
      default: (item) => item,
    },
    getPatchData: {
      type: Function,
      required: false,
      default: (item) => {
        let { id, __typename, ...patchItem } = item;
        return patchItem;
      },
    },
    isCreate: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    dialog: {
      get() {
        return this.value;
      },
      set(newValue) {
        this.$emit("input", newValue);
      },
    },
  },
  methods: {
    save() {
      this.loading = true;

      if (
        !this.itemModel ||
        (this.isCreate && !this.gqlCreateMutation) ||
        (!this.isCreate && !this.gqlPatchMutation)
      )
        return;

      let mutation = this.isCreate
        ? this.gqlCreateMutation
        : this.gqlPatchMutation;

      let variables = this.isCreate
        ? { input: this.getCreateData(this.itemModel) }
        : { input: this.getPatchData(this.itemModel), id: this.itemModel.id };

      this.$apollo
        .mutate({
          mutation: mutation,
          variables: variables,
          update: (store, data) => {
            this.$emit(
              "update",
              store,
              data.data[mutation.definitions[0].name.value].item,
            );
          },
        })
        .then((data) => {
          this.$emit("save", data);

          this.handleSuccess();
        })
        .catch((error) => {
          console.error(error);
          this.$emit("error", error);

          this.$toastError();
        })
        .finally(() => {
          this.loading = false;
          this.dialog = false;
        });
    },
    dynamicSetter(item, fieldName) {
      return (value) => {
        this.$set(item, fieldName, value);
      };
    },
    buildExternalSetter(item) {
      return (fieldName, value) => this.dynamicSetter(item, fieldName)(value);
    },
    buildAttrs(item, field) {
      return {
        dense: true,
        filled: true,
        value: item[field.value],
        inputValue: item[field.value],
        label: field.text,
      };
    },
    buildOn(setter) {
      return {
        input: setter,
        change: setter,
      };
    },
    handleSuccess() {
      let snackbarTextKey = this.isCreate
        ? this.createSuccessMessageI18nKey
        : this.editSuccessMessageI18nKey;

      this.$toastSuccess(snackbarTextKey);
      this.resetModel();
    },
    resetModel() {
      this.itemModel = JSON.parse(
        JSON.stringify(this.isCreate ? this.defaultItem : this.editItem),
      );
    },
    updateModel() {
      // Only update the model if the dialog is hidden or has just been mounted
      if (this.forceModelItemUpdate || !this.firstInitDone || !this.dialog) {
        this.resetModel();
      }
    },
  },
  mounted() {
    this.updateModel();
    this.firstInitDone = true;

    this.$watch("isCreate", this.updateModel);
    this.$watch("defaultItem", this.updateModel, { deep: true });
    this.$watch("editItem", this.updateModel, { deep: true });
  },
};
</script>

<style scoped></style>
